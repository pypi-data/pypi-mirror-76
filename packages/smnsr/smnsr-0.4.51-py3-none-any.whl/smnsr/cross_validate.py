from smnsr.models import SMNSR, Y_HAT
from smnsr.patients import AugmentedTADPOLEData, TADPOLEData
from smnsr.models import TO
from sklearn.model_selection import KFold
from argparse import ArgumentParser
import sys
from pytictoc import TicToc
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import numpy as np


def perform_cv(args):
    splitter = KFold(args.folds, random_state=0, shuffle=True)
    data = TADPOLEData(
        data=args.modality_path + args.data_file,
        modality_path=args.modality_path,
        modality_k=args.modality_k,
    )

    # Split the ptids into n folds
    ptids = data.get_ptids(min_time_points=2, target=args.target)
    print("Total patients in CV: %i" % len(ptids))
    t = TicToc()
    print("CV mode %s" % args.mode)
    sys.stdout.flush()
    predictions = []
    modality_ranks = []
    for fold, (train_index, test_index) in enumerate(splitter.split(ptids)):
        print("Fold %i/%i" % (fold, args.folds - 1))
        sys.stdout.flush()
        train_ptids = [ptids[i] for i in train_index]
        test_ptids = [ptids[i] for i in test_index]
        aug_data = AugmentedTADPOLEData(
            data, args.precomputed_path + "merged_%i.p" % fold, train_ptids
        )
        model = SMNSR(aug_data, n_jobs=args.cpus, forecast=False, mode=args.mode)
        print("Fitting model")
        t.tic()
        model.fit(train_ptids)
        print("Trainig took %s seconds" % t.tocvalue())
        print("Performing forecasting")
        sys.stdout.flush()
        # Fetch known target values for the patients
        y = aug_data.getY(test_ptids, target=args.target)
        prediction_definition = y[[TADPOLEData.PTID, TADPOLEData.C_MONTH]]
        print(
            "Patients with more than one measurement in fold %i: %i"
            % (fold, y[TADPOLEData.PTID].unique().shape[0])
        )

        y_hat = model.predict(prediction_definition, target=args.target)
        prediction = y.merge(
            y_hat,
            left_on=[TADPOLEData.PTID, TADPOLEData.C_MONTH],
            right_on=[TADPOLEData.PTID, TO],
        )
        predictions.append((prediction))
        modality_ranks.append(model.ranked_modalities)
        fold += 1

    predictions = pd.concat(predictions, ignore_index=True)
    with open(args.output_path + args.result_file_name, "wb") as file:
        pickle.dump(prediction, file)
    evaluate_predictions(predictions, data)

    return prediction


def evaluate_predictions(predictions, data):

    patient_info = data.get_features(
        data.get_ptids(), [TADPOLEData.DX_BL, TADPOLEData.AGE]
    )

    predictions = predictions.merge(
        patient_info,
        left_on=[TADPOLEData.PTID, TADPOLEData.C_MONTH],
        right_on=[TADPOLEData.PTID, TADPOLEData.C_MONTH],
        how="left",
    )

    # Evaluate overall performance
    y_hat = predictions[Y_HAT].values
    y = predictions[AugmentedTADPOLEData.Y].values
    print("Total patients: %i" % (predictions[TADPOLEData.PTID].unique().shape[0]))
    overall_mae = mean_absolute_error(y_hat, y)
    overall_rmse = mean_squared_error(y_hat, y)
    print("Overall MAE: %f" % overall_mae)
    print("Overall RMSE: %f" % overall_rmse)
    distances = {}
    unique_months = predictions[TADPOLEData.C_MONTH].unique()

    # Plot predictions

    def mae(data: pd.DataFrame, month: int):
        y_hat = data[data[TADPOLEData.C_MONTH] == month][Y_HAT]
        y = data[data[TADPOLEData.C_MONTH] == month][AugmentedTADPOLEData.Y]
        if y.empty or y_hat.empty:
            return np.nan
        return mean_absolute_error(y_hat, y)

    def rmse(data: pd.DataFrame, month: int):
        y_hat = data[data[TADPOLEData.C_MONTH] == month][Y_HAT]
        y = data[data[TADPOLEData.C_MONTH] == month][AugmentedTADPOLEData.Y]
        if y.empty or y_hat.empty:
            return np.nan
        return mean_squared_error(y_hat, y, squared=False)

    for m in unique_months:
        distances[m] = {}
        distances[m]["combined"] = (mae(predictions, m), rmse(predictions, m))
        for diagnosis in predictions[TADPOLEData.DX_BL].unique():
            patients_with_diagnosis = predictions[
                predictions[TADPOLEData.DX_BL].isin([diagnosis])
            ]
            distances[m][diagnosis] = (
                mae(patients_with_diagnosis, m),
                rmse(patients_with_diagnosis, m),
            )
    print("Pointwise MAE:")
    for i, (group, month) in enumerate(distances.items()):
        print("\t%s" % group)
        for j, (k, v) in enumerate(month.items()):
            print("\t\t %s: %f %f" % (k, v[0], v[1]))
    sys.stdout.flush()


def parse_args(cli_args):
    cli = ArgumentParser()
    cli.add_argument("--folds", type=int, default=10)
    cli.add_argument("--precomputed", action="store_true")
    cli.add_argument("--modality_path", type=str, default="../../modalities/")
    cli.add_argument(
        "--precomputed_path", type=str, default="../../output/precomputed_folds/"
    )
    cli.add_argument("--data_file", type=str, default="TADPOLE_D1_D2.csv")
    cli.add_argument("--target", type=str, default="ADAS13")
    cli.add_argument("--bl_forecast", default=False, action="store_true")
    cli.add_argument("--output_path", type=str, default="../../output/")
    cli.add_argument("--result_file_name", type=str, default="cv_result.p")
    cli.add_argument("--modality_k", type=int, default=8)
    cli.add_argument("--cpus", type=int, default=None)
    cli.add_argument("--mode", type=str, default="xgb")

    return cli.parse_args(cli_args)
