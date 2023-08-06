import numpy as np

from sklearn.linear_model import HuberRegressor
from sklearn.neighbors import NearestNeighbors
from scipy import stats
from smnsr.models import FROM, TO, PTID, FORECAST_Y
from sklearn.preprocessing import StandardScaler
from sklearn.base import clone
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
import pandas as pd
import re

FORECAST = "forecast"
SIMILARITIES = "similarities"
STD = "std"
SKEW = "skew"
FUTURE_MIN = "min"
FUTURE_MAX = "max"
BASELINE = "value"


def weightedL2(a,b,**kwargs):
    weight = kwargs["w"]
    q = a-b
    return np.sqrt((weight*(q*q)).sum())

class KNNSR:

    def __init__(self, tadpole_data,
                 n_neighbors=400,
                 aligning_n_neighbors=30,
                 modality="cognitive2",
                 target_value='ADAS13',
                 n_jobs = 16,
                 column_weights = [['AGE', 5], ['DX', 5], ['ADAS13', 5]]):
        self.tadpole_data = tadpole_data
        self.n_neighbors = n_neighbors
        self.aligning_n_neighbors = aligning_n_neighbors
        self.column_weights = column_weights
        self.modality = modality
        self.target_value = target_value
        self.n_jobs = n_jobs
        self.scaler = StandardScaler()
        self.fitted = False
        #self.regression_models = {"rf_forecast":RandomForestRegressor(n_estimators=10, n_jobs=4), "hr_forecast":HuberRegressor(fit_intercept=True, max_iter=200)}
        self.regression_models = {"hr_forecast":HuberRegressor(fit_intercept=True, max_iter=200)}
        self.training_ptids = []

    def __create_distance_weights(self, data):

        weight_vector = np.ones((1, len(data.columns)))
        for c in self.column_weights:
            p = re.compile('^'+c[0])
            column_indexes = [ i for i,f in enumerate(data.columns) if p.match(f) ]

            weight_vector[0, column_indexes] = c[1]
        return weight_vector

    def fit(self, x, y=0):
        self.training_ptids = x
        self.training_x,self.training_y, self.training_meta = self.tadpole_data.getXY(x,self.modality,self.target_value,retrieve_meta=True,include_target=True)
        weights = self.__create_distance_weights(self.training_x)

        self.scaler.fit(self.training_x)
        self.training_x = self.scaler.transform(self.training_x)

        knn = NearestNeighbors(n_neighbors=self.n_neighbors,
                               n_jobs=self.n_jobs, metric=weightedL2,
                               metric_params={ 'w' : weights}
                               )
        self.knn_model = knn.fit(self.training_x)
        self.fitted = True

    def predict(self, x,y=None):
        """
        For compatibility with sklearn, perform predictions on an input matrix of
        two columns consisting ptids and time_points
        """
        forecast_list = {}
        similarities_list = {}
        std_list = {}
        skew_list = {}
        min_list = {}
        max_list = {}
        value_list = {}

        if isinstance(x,np.ndarray):
            n_samples = x.shape[0]
            predicted_timepoints = x[:,2]
        else:
            n_samples = x[0].shape[0]
            predicted_timepoints = [ x[1] for i in range(0,n_samples)]
            x = x[0]
        if y is None:
            y = np.zeros(predicted_timepoints[0].shape[0])

        for pt in range(0, n_samples):
            assert self.tadpole_data.has_modality(x[pt, 0], self.modality)

            forecasted, similarities, std, skew, v_min, v_max, v_value = self.predict_slope(x[pt, :],
                                                                                            predicted_time_points=
                                                                                            predicted_timepoints[pt],
                                                                                            d3=False)

            forecast_list[x[pt, 0]] = forecasted
            similarities_list[x[pt, 0]] = similarities
            std_list[x[pt, 0]] = std
            skew_list[x[pt, 0]] = skew
            min_list[x[pt, 0]] = v_min
            max_list[x[pt, 0]] = v_max
            value_list[x[pt, 0]] = v_value

        prediction = {FORECAST:forecast_list,
                     SIMILARITIES:similarities_list,
                     STD:std_list,
                     SKEW:skew_list,
                     FUTURE_MIN:min_list,
                     FUTURE_MAX:max_list,
                     BASELINE:value_list
                     }
        return self.__to_list(x, y, prediction,predicted_timepoints)

    def predict_slope(self, pt_data, predicted_time_points, d3=False):

        ptid = str(pt_data[0])
        start_point = int(float(pt_data[1]))

        if predicted_time_points.shape == ():
            predicted_time_points = np.expand_dims(predicted_time_points,axis=0)

        predicted_time_points = predicted_time_points.astype(float)

        starting_y_values = []
        y_values = []
        future_y_values = []
        time_points = []

        ptids = []

        query_features, _ = self.tadpole_data.getXY([ptid], self.modality, target=self.target_value,time_points=[start_point],include_target=True,impute_ptids=self.training_ptids)

        dist, ind = self.knn_model.kneighbors(self.scaler.transform(query_features))
        dist = dist[0]
        ind = ind[0]

        neighbor_time_points = self.training_meta[self.tadpole_data.C_MONTH].tolist()
        neighbor_ptids = self.training_meta[self.tadpole_data.PTID].tolist()

        unique_ptids = []
        matching_time_points = []
        unique_ptid_count = 0

        #Select n patients from the neighborhood
        for i in range(0, ind.shape[0]):
            if neighbor_ptids[i] in unique_ptids or neighbor_ptids[i] == ptid:
                continue
            if unique_ptid_count == self.aligning_n_neighbors:
                break
            unique_ptids.append(neighbor_ptids[ind[i]])
            matching_time_points.append(neighbor_time_points[ind[i]])
            unique_ptid_count += 1

        neighbor_ptids = unique_ptids

        target_x, target_y = self.tadpole_data.getXY( [ptid],self.modality, target=self.target_value,time_points=[start_point],impute_ptids=self.training_ptids)
        target_y = target_y.values

        for i,n_ptid in enumerate(neighbor_ptids):
            queried_time_point = matching_time_points[i]

            x_measurement, y_measurement, metadata = self.tadpole_data.getXY([n_ptid],self.modality,target=self.target_value,retrieve_meta=True,impute_ptids=self.training_ptids)

            matching_y_value = y_measurement[ metadata[self.tadpole_data.C_MONTH] == queried_time_point].values[0]

            xy_timepoints = metadata[self.tadpole_data.C_MONTH]

            xy_timepoints -= queried_time_point

            if xy_timepoints.shape[0] == 0:
                print('No features for patient: %s'%(str(neighbor_ptids[i])))
                continue

            y_values.append(y_measurement.values)
            future_y_values.append( y_measurement[ xy_timepoints >= 0].values)
            time_points.append(xy_timepoints.values)

            starting_y_values.append(np.tile(matching_y_value, y_measurement.shape[0]))
            ptids.append(str(neighbor_ptids[i]))
        # Stack the lists

        y_values = np.hstack(y_values)
        future_y_values = np.hstack(future_y_values)
        starting_y_values = np.hstack(starting_y_values)
        time_points = np.hstack(time_points)
        # Change dtypes
        y_values = y_values.astype('float64')
        time_points = time_points.astype('float64')
        # Sort the stacked lists
        sorted_indexes = np.argsort(time_points)
        starting_y_values = starting_y_values[sorted_indexes]
        y_values = y_values[sorted_indexes]
        time_points = time_points[sorted_indexes]
        # Calculate population statistics
        value_min = np.min(future_y_values)
        value_max = np.max(future_y_values)
        value_current = target_y

        untransformed_train_features = np.hstack(
            (np.expand_dims(time_points, axis=1), np.expand_dims(starting_y_values, axis=1)))

        features = untransformed_train_features

        # try:

        regression_models = {}

        for _,(k,model) in enumerate(self.regression_models.items()):
            regression_models[k] = clone(model)
            regression_models[k].fit(features, y_values.ravel())

        untransformed_features = np.hstack((np.expand_dims( np.hstack((0,predicted_time_points-start_point)), axis=1),np.tile(target_y, (predicted_time_points.shape[0]+1, 1))))
        features = untransformed_features.astype(float)

        predictions = {}
        for _,(key,model) in enumerate(regression_models.items()):

            regression_forecast = np.expand_dims(model.predict(features), axis=1)
            regression_forecast = regression_forecast +target_y - regression_forecast[0]
            regression_forecast = regression_forecast[1:,:]
            predictions[key] = regression_forecast

        similarities = np.mean(dist)
        std = np.std(dist)
        skew = stats.skew(dist)
        return predictions, similarities, std, skew, value_min, value_max, value_current[0]

    def __to_list(self,x,y, prediction,forecast_timepoints):

        column_names = []
        predictions = []
        for i in range(0,x.shape[0]):
            ptid = x[i,0]
            from_time_point = x[i,1]
            if len(column_names) == 0:
                column_names = [PTID, FORECAST_Y,FROM, TO]
                column_names += list(prediction.keys())
                column_names += prediction["forecast"][ptid].keys()
                column_names.remove("forecast")

            values = []
            for key in prediction.keys():
                if key != "forecast":
                    values.append([prediction[key][ptid]][0])
            for t in range(0, len(forecast_timepoints[i])):
                to_time_point = forecast_timepoints[i][t]

                regression_values = []
                for i, (k, f) in enumerate(prediction["forecast"][ptid].items()):
                    regression_values.append(float(f[t, 0]))

                predictions.append([ptid, float(y[t]),float(from_time_point), float(to_time_point)] + values + regression_values)

        return (predictions,column_names)