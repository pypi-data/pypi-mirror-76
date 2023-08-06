import pandas as pd
from smnsr.models import KNNSR
import numpy as np
import logging
from smnsr.patients import TADPOLEData
import psutil
import ray
import sys


def create_features(
    tadpole_data: TADPOLEData,
    train_ptids,
    test_ptids,
    modalities=None,
    return_knn=False,
    num_cpus=None,
):

    if not num_cpus:
        num_cpus = psutil.cpu_count(logical=False)

    tadpole_data.set_backend("pandas")

    df_id = ray.put(tadpole_data)

    if modalities is None:
        modalities = tadpole_data.modality_names

    avg = len(train_ptids) / float(num_cpus)
    split_train_ids = []
    split_test_ids = []
    last = 0.0

    timeseries_features = {}
    knn_models = {}

    while last < len(train_ptids):
        split_train_ids.append(train_ptids[int(last) : int(last + avg)])
        last += avg
    last = 0.0
    avg = len(test_ptids) / float(num_cpus)
    while last < len(test_ptids):
        split_test_ids.append(test_ptids[int(last) : int(last + avg)])
        last += avg

    def process_ptids(ptids, m, t, df_id, knn_id):
        result_ids = [
            create_pt_series.remote(df_id, knn_id, m, t, ptids[i])
            for i in range(num_cpus)
        ]
        results = ray.get(result_ids)
        return pd.concat(results, ignore_index=False)

    for m in modalities:
        sys.stdout.flush()
        timeseries_features[m] = {}
        if m == "adas13":
            continue
        if return_knn:
            knn_models[m] = {}

        for t in tadpole_data.Y_FEATURES:

            knn = KNNSR(tadpole_data, modality=m, target_value=t)
            knn.fit(train_ptids)
            knn_id = ray.put(knn)

            train_ts = process_ptids(split_train_ids, m, t, df_id, knn_id)
            if len(test_ptids) > 0:
                test_ts = process_ptids(split_test_ids, m, t, df_id, knn_id)
                results = pd.concat([train_ts, test_ts], ignore_index=False)
            else:
                results = train_ts
            timeseries_features[m][t] = results
        if return_knn:
            knn_models[m][t] = knn

    return timeseries_features, knn_models


@ray.remote
def create_pt_series(df, knn, feature_modality, target, train_ptids):

    column_names = []

    predictions = []
    for ptid in train_ptids:

        logging.getLogger(__name__).debug("Patient %s" % (ptid))

        features, y, modality_metadata = df.getXY(
            [ptid],
            feature_modality,
            target,
            retrieve_meta=True,
            impute_ptids=train_ptids,
        )
        feature_time_points = modality_metadata[df.C_MONTH].values

        # Targets are are unimputed data
        target_features = df.get_features([ptid], [target])
        target_time_points = target_features[df.C_MONTH].values
        target_features = target_features[target].values

        sorted_indexes = np.argsort(feature_time_points)
        feature_time_points = feature_time_points[sorted_indexes]

        sorted_indexes = np.argsort(target_time_points)
        target_time_points = target_time_points[sorted_indexes]
        target_features = target_features[sorted_indexes]

        if target_features.shape[0] < 1 or feature_time_points.shape[0] < 1:
            logging.getLogger(__name__).debug(
                "Patient %s measuremets or target value. "
                "Number of measurements: %i, Number of target values %i. Skipping"
                % (target, features.shape[0], target_features.shape[0])
            )
            continue

        for m in range(0, len(feature_time_points)):
            from_time_point = feature_time_points[m]

            forecast_timepoints = target_time_points[
                from_time_point < target_time_points
            ]
            y_true = target_features[from_time_point < target_time_points]
            if forecast_timepoints.shape[0] == 0:
                break

            x = (np.array([[ptid, from_time_point]]), forecast_timepoints)
            prediction = knn.predict(x, y_true)

            if len(column_names) == 0:
                column_names = prediction[1]
            predictions += prediction[0]

    return pd.DataFrame(data=predictions, columns=column_names)


def augment_ts(x, y, times, std):
    x_temp = np.tile(x, (times, 1))
    y_temp = np.tile(y, (times, 1))

    for c in range(0, x_temp.shape[1]):
        if np.unique(x_temp[:, c]).shape[0] < 3:
            continue

        x_temp[:, c] += np.random.normal(0, std, (x_temp.shape[0],))

    x = np.vstack((x, x_temp))
    y = np.vstack((y, y_temp))

    return x, y
