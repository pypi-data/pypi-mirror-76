from smnsr.models import Y_HAT
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.dummy import DummyRegressor
from xgboost import XGBRFRegressor
import multiprocessing
from smnsr.patients import TADPOLEData
from smnsr.patients import AugmentedTADPOLEData
from smnsr.models import KNNSR
from smnsr.models.knn import BASELINE, FUTURE_MAX, FUTURE_MIN
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, make_scorer
from pytictoc import TicToc
from sklearn.base import RegressorMixin, TransformerMixin
from smnsr.models import BaseStackedModel, FROM, TO

# TODO: Add interaction_constraints
# TODO: Add early stopping using validation set

KNNSR_BYPASS = "_forecast"


class SMNSR(BaseStackedModel):
    def __init__(
        self,
        data: AugmentedTADPOLEData,
        training_cv_folds=5,
        n_jobs=None,
        verbosity=0,
        mode="xgb",
        forecast_min="baseline",
        forecast_max=None,
        max_modalities=1,
        forecast=False,
    ):
        super().__init__(data)

        self.training_cv_folds = 5
        self.verbosity = verbosity
        self.forecast_min = forecast_min
        self.forecast_max = forecast_max
        self.mode = mode
        self.max_modalities = max_modalities
        self.forecast = forecast
        if not n_jobs:
            n_jobs = multiprocessing.cpu_count()
        self.n_jobs = n_jobs

        self.__create_pipeline()

        self.fold_generator = KFold(n_splits=training_cv_folds)

        self.ranked_modalities = []
        self.knnsrs = {}

    def __create_pipeline(self):
        if self.mode == "bypass_knnsr":
            pipeline = [("regression", KNNSRBypassRegression(column=KNNSR_BYPASS))]
            self.pipeline_params = {}
            self.n_jobs = 1
            self.training_cv_folds = 2

        if self.mode == "xgb":
            pipeline = [
                ("variance_treshold", VarianceThreshold()),
                ("scale", StandardScaler()),
                ("regression", XGBRFRegressor()),
            ]
            self.pipeline_params = {
                "regression__n_estimators": [100, 200, 400, 800],
                "regression__max_depth": [1, 3, 5, 7, 11],
                "regression__subsample": [0.5, 1],
                "regression__colsample_bylevel": [0.8, 1],
                "regression__random_state": [0],
                "regression__eval_metric": ["mae"],
                "regression__reg_lambda": [0, 1],
                "regression__reg_alpha": [0, 1],
                "regression__objective": ["reg:squarederror"],
            }
        if self.mode == "linear":
            pipeline = [
                (
                    "filter",
                    FilterColumns(
                        columns=[BASELINE, AugmentedTADPOLEData.FORECAST_DIST]
                    ),
                ),
                ("scale", StandardScaler()),
                ("polynomial_features", PolynomialFeatures()),
                ("regression", LinearRegression()),
            ]
            self.pipeline_params = {}
            self.n_jobs = 1

        self.pipeline = Pipeline(pipeline)

    def fit(self, ptids, target="ADAS13"):

        ptids, _ = super()._process_x(ptids)

        self.training_ptids = ptids
        self.target = target

        self.ranked_modalities = []
        modalities = self.data.get_modalities()
        tictoc = TicToc()

        # Create a fall-back regressor guessing the target mean

        self.fallback = DummyRegressor(strategy="mean")
        target_values = self.data.getY(ptids, target, drop_baseline=False)[
            AugmentedTADPOLEData.Y
        ]
        self.fallback.fit(target_values, target_values)
        # If we are not using precalculated features, KNNSR models need to be trained.
        for i, modality in enumerate(modalities):

            if self.forecast:
                if self.verbosity == 2:
                    print("\tFitting KNNSR for %s" % modality)
                knn = KNNSR(self.data.data, modality=modality, target_value=target)
                knn.fit(ptids)
                self.knnsrs[modality] = knn

            if self.verbosity > 0:
                print(
                    "\tFitting %s for %s (%i/%i)"
                    % (self.mode, modality, i, len(modalities))
                )
            tictoc.tic()
            x, y, t = self.data.getXY(ptids, modality, target=target)
            # If none of the patients in the training set have the modality, return a DummyClassifier guessing the mean
            # of the target.
            if x.shape[0] == 0:
                self.ranked_modalities.append((np.inf, modality, self.fallback))
                if self.verbosity == 2:
                    print("\tNo samples for %s in training set" % modality)
                continue

            # Fit model with CV. Store the model and score
            grid = GridSearchCV(
                self.pipeline,
                cv=self.fold_generator,
                n_jobs=self.n_jobs,
                param_grid=self.pipeline_params,
                verbose=0,
                scoring=make_scorer(mean_absolute_error, greater_is_better=False),
            )
            grid.fit(x, y)
            if self.verbosity == 2:
                print(
                    "\tTraining for %s took %f"
                    % (modality, tictoc.tocvalue(restart=True))
                )
            self.ranked_modalities.append(
                (grid.best_score_, modality, grid.best_estimator_, grid.best_params_)
            )

        # Rank modalities according to score.
        self.ranked_modalities = sorted(
            self.ranked_modalities, key=lambda l: l[0], reverse=True
        )
        if self.verbosity == 2:
            for i, m in enumerate(self.ranked_modalities):
                print("\t%i %s %f" % (i, m[1], m[0]))

    def is_fitted(self):
        return len(self.ranked_modalities) > 0

    def predict(
        self,
        x,
        target,
        step_size=1,
        forecast_start="2018-01-01",
        forecast_end="2022-12-01",
    ):

        assert self.is_fitted()

        forecast_definition, nan_mask = super()._create_forecast_definition(
            x,
            forecast_start=forecast_start,
            forecast_end=forecast_end,
            step_size=step_size,
        )

        patients = forecast_definition[TADPOLEData.PTID].unique()

        results = []
        # Loop over the patients
        for i, ptid in enumerate(patients):

            target_time_points = sorted(
                forecast_definition[forecast_definition[TADPOLEData.PTID] == ptid][
                    TADPOLEData.C_MONTH
                ].values.tolist()
            )
            patient_time_points = self.data.data.get_patient_time_points(ptid)
            start_time_points = [patient_time_points[-1]]

            if self.forecast:
                if self.verbosity > 1:
                    print("%i/%i" % (i, len(patients)))
                modality_count = 0
                prediction = None
                for i, modality in enumerate(self.ranked_modalities):
                    if not self.data.data.has_modality(
                        ptid,
                        modality[1],
                        time_points=start_time_points,
                        target=None,
                        nan_mask=nan_mask,
                    ):
                        continue
                    # Get features from the lower stack.
                    x = (
                        np.array([[ptid, start_time_points[0]]]),
                        start_time_points[0] + np.array(target_time_points),
                    )
                    knnsr_predictions = self.knnsrs[modality[1]].predict(x)
                    xy_measurement = self.data.data.getXY(
                        [ptid],
                        modality[1],
                        target=target,
                        split=False,
                        impute_ptids=self.training_ptids,
                    )
                    knnsr_predictions = self.data.merge_view(
                        xy_measurement,
                        pd.DataFrame(
                            data=knnsr_predictions[0], columns=knnsr_predictions[1]
                        ),
                    )
                    x, y, t = self.data.getXY(
                        [ptid],
                        modality[1],
                        target=target,
                        start_time_points=start_time_points,
                        target_time_points=start_time_points[0]
                        + np.array(target_time_points),
                        knnsr_prediction=knnsr_predictions,
                    )
                    if x.shape[0] > 0:
                        y_hat = modality[2].predict(x)
                        y_hat = self.__cap_prediction(y_hat.ravel(), x)
                        if self.verbosity > 1:
                            print("Utilizing %s for patient %s" % (modality[1], ptid))
                        if modality_count == 0:
                            prediction = t
                            prediction[FROM] = prediction[FROM] + start_time_points[0]
                            prediction[TO] = prediction[TO] + start_time_points[0]
                            prediction[Y_HAT] = y_hat
                            prediction[TADPOLEData.PTID] = ptid
                        if modality_count > 0:
                            prediction[Y_HAT] = prediction[Y_HAT] + y_hat
                        modality_count += 1
                        if modality_count >= self.max_modalities:
                            break
                assert prediction is not None, "Prediction was None for %" % ptid
                prediction[Y_HAT] = prediction[Y_HAT] / modality_count
                results.append(prediction)
            else:
                patient_time_points = self.data.data.get_patient_time_points(ptid)
                start_time_points = [patient_time_points[0]]

                for target_time in target_time_points:

                    modality_count = 0
                    prediction = None

                    for i, modality in enumerate(self.ranked_modalities):
                        x, y, t = self.data.getXY(
                            [ptid],
                            modality[1],
                            target=target,
                            start_time_points=start_time_points,
                            target_time_points=[target_time],
                        )
                        if x.shape[0] > 0:
                            y_hat = modality[2].predict(x)
                            y_hat = self.__cap_prediction(y_hat, x)

                            if modality_count == 0:
                                prediction = t
                                prediction[Y_HAT] = y_hat
                                prediction[TADPOLEData.PTID] = ptid
                            if modality_count > 0:
                                prediction[Y_HAT] = prediction[Y_HAT] + y_hat[0]
                            modality_count += 1
                            if modality_count >= self.max_modalities:
                                break
                    if modality_count > 0:
                        prediction[Y_HAT] = prediction[Y_HAT] / modality_count
                    assert prediction is not None, (
                        "No modalities modalities for patient %s" % ptid
                    )
                    results.append(prediction)
        results: pd.DataFrame = pd.concat(results)
        patient_data = self.data.data.get_features(
            results[TADPOLEData.PTID].unique(), []
        )[[TADPOLEData.PTID, TADPOLEData.RID]]
        results = results.merge(
            patient_data,
            right_on=TADPOLEData.PTID,
            how="right",
            left_on=TADPOLEData.PTID,
        )
        return results

    def __cap_prediction(self, y_hat, x):
        if self.forecast_min == "baseline":
            return np.maximum(y_hat, x[BASELINE].values)
        if self.forecast_min == "future":
            return np.maximum(y_hat, x[FUTURE_MIN].values)
        if self.forecast_max == "future":
            return np.minimum(y_hat, x[FUTURE_MAX].values)


class KNNSRBypassRegression(RegressorMixin):
    def __init__(self, column="forecast"):
        self.column = column

    def fit(self, X=None, y=None):
        assert isinstance(X, pd.DataFrame)
        self.bypassed_features = [
            c for i, c in enumerate(X.columns) if c.endswith(self.column)
        ]
        return self

    def predict(self, X=None):
        # If e.g. predictions from several KNN regressors are passed, return the mean
        if len(self.bypassed_features) > 1:
            return np.mean(X.values[:, self.bypassed_features], axis=1)
        return X[self.bypassed_features].values


class FilterColumns(TransformerMixin):
    def __init__(self, columns, exclude=False):
        self.__columns = columns
        self.__exclude = exclude

    def fit(self, X, y=None):
        return self

    def transform(self, x, y=None):
        if self.__exclude:
            return x[[c for c in x.columns if c not in self.__columns]]
        return x[self.__columns]
