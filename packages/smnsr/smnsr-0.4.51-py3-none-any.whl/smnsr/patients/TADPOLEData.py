"""
Created on Fri Oct 13 17:15:12 2017

@author: ciszek
"""

import pandas as pd
import vaex as vx
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import re
from sklearn.impute import KNNImputer
import itertools
import yaml
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pkg_resources


class TADPOLEData:

    PTID = "PTID"
    RID = "RID"
    VISCODE = "VISCODE"
    DX = "DX"
    DX_MAPPED = "DX_MAPPED"
    DX_BL = "DX_bl"
    CN = "CN"
    MCI = "MCI"
    AD = "AD"
    C_MONTH = "M"
    AGE = "AGE"
    DN = ["D1", "D2"]
    EXAM_DATE = "EXAMDATE"
    YEARS_BL = "Years_bl"
    RELATIVE_VENTRICLE_VOLUME = "RelativeVentricleVolume"
    ICV = "ICV"
    VENTRICLES = "Ventricles"
    IMPUTED = "imputed"
    Y_FEATURES = ["ADAS13"]
    DEFAULT_IMPUTE_MODALITY = "patient"
    CATEGORICAL = [
        "PTEDUCAT",
        "DXCHANGE",
        "APOE4",
        DX,
        DX_BL,
        "PTGENDER",
        "PTETHCAT",
        "PTRACCAT",
        "PTMARRY",
    ]
    META = [PTID, RID, C_MONTH, EXAM_DATE, YEARS_BL, VISCODE, DX_MAPPED, DX_BL]
    MODALITY_YAML = "modalities.yaml"

    ONE_HOT_ENCODED = {}

    def __init__(
        self,
        data,
        modality_path=None,
        modality_k=7,
        verbosity=2,
        challenge_filter=True,
    ):

        self.verbosity = verbosity
        if verbosity == 2:
            print("Reading data")
        if modality_path is None:
            modality_path = pkg_resources.resource_filename(
                __name__, "/../modalities/"
            )

        assert isinstance(data, str) or isinstance(
            data, pd.DataFrame
        ), "Input data must be specified as a filepath or as a DataFrame"
        if isinstance(data, str):
            self._df = pd.read_csv(data, low_memory=False)
        else:
            self._df = data.copy()
        self.df_raw = self._df.copy()

        if verbosity == 2:
            print("Correcting age")
        self._df = self.__correct_age(self._df)
        if verbosity == 2:
            print("Adding relative ventricle volume")
        self._df = self.__add_relative_ventricle_volume(self._df)

        self._df = self.__propagate_dx(self._df)

        if verbosity == 2:
            print("One hot encoding data")
        self._df, self.one_hot_column_map, self.encoders = self.__one_hot_encode(
            self._df
        )

        if verbosity == 2:
            print("Translating clinical status")
        self._df = self.__translate_clinical_status(self._df)
        self.__load_modalities(modality_path)

        self.relevant_columns = []
        for m in self.modality_columns:
            self.relevant_columns += self.modality_columns[m]

        self.relevant_columns += self.META
        self._df = self._df[self.relevant_columns]

        if verbosity == 2:
            print("Correcting non-numeric entries")
        self._df = self.__correct_non_numeric_entries(self._df)

        if verbosity == 2:
            print("Total patients: %i" % (np.unique(self._df["PTID"]).shape[0]))

        self.one_hot_encoded = {}
        if verbosity == 2:
            print("Creating modality combinations")
        self.__create_modality_combinations(modality_k)
        if verbosity == 2:
            print("Adding patient columns")
        self.__add_patient_columns()

        self.modality_names = self.get_modalities()

        self.set_backend("pandas")

        if challenge_filter:
            self.use_challenge_modalities()

    def set_backend(self, backend="pandas"):
        self.backend = pd
        if self.verbosity == 2:
            print("Backend set to %s" % backend)

    def __load_modalities(self, modality_path):
        self.modality_columns = {}
        with open(modality_path + self.MODALITY_YAML) as file:
            modalities = yaml.full_load(file)
            for modality_name in modalities.keys():
                self.modality_columns[
                    modality_name
                ] = self.__translate_one_hot_encoded_columns(modalities[modality_name])

    def __translate_clinical_status(self, df):
        def map_status(value):
            if value == "NL" or value == "MCI to NL":
                return self.CN
            if value == "MCI" or value == "NL to MCI" or value == "Dementia to MCI":
                return self.MCI
            if (
                value == "Dementia"
                or value == "NL to Dementia"
                or value == "MCI to Dementia"
            ):
                return self.AD

            return pd.NA

        df[self.DX_MAPPED] = df[self.DX]
        df[self.DX_MAPPED] = df[self.DX_MAPPED].map(map_status)
        return df

    def __correct_age(self, data):
        data[self.AGE] += data[self.YEARS_BL]
        return data

    def __add_relative_ventricle_volume(self, data):
        data[self.RELATIVE_VENTRICLE_VOLUME] = data[self.VENTRICLES] / data[self.ICV]
        return data

    def __correct_non_numeric_entries(self, data_file):
        dtypes = data_file.dtypes
        for c in range(1, data_file.shape[1]):

            if data_file.columns[c] in self.META:
                continue
            if dtypes[c] == "float64":
                continue

            if np.issubdtype(dtypes[c], np.object):
                data_file.loc[:, data_file.columns[c]] = data_file.loc[
                    :, data_file.columns[c]
                ].astype("str")

            data_file.loc[:, data_file.columns[c]] = data_file.loc[
                :, data_file.columns[c]
            ].str.replace(" ", "")
            data_file.loc[:, data_file.columns[c]] = data_file.loc[
                :, data_file.columns[c]
            ].str.replace("<", "")
            data_file.loc[:, data_file.columns[c]] = data_file.loc[
                :, data_file.columns[c]
            ].str.replace(">", "")
            data_file.loc[:, data_file.columns[c]].replace(
                r"^\s*$", np.nan, regex=True, inplace=True
            )
            try:
                data_file.loc[:, data_file.columns[c]] = data_file.loc[
                    :, data_file.columns[c]
                ].astype("float32")
            except ValueError as e:
                print(data_file.columns[c])
                print(e)
        return data_file

    def __one_hot_encode(self, data_file: pd.DataFrame, encoders=None):

        dtype_dict = {}

        one_hot_column_map = {}

        if encoders is None:
            encoders = {}

        for value in self.CATEGORICAL:
            if value in data_file.columns:
                dtype_dict[value] = "object"

        data_file = data_file.astype(dtype=dtype_dict)

        for c in range(1, data_file.shape[1]):

            if data_file.columns[c] in self.META:
                continue

            if data_file.columns[c] in self.CATEGORICAL:

                non_nan_indexes = np.where(
                    data_file.loc[:, data_file.columns[c]].notnull()
                )[0]
                if non_nan_indexes.shape[0] == 0:
                    continue
                if data_file[data_file.columns[c]].apply(lambda x: x == " ").any():
                    continue

                if not data_file.columns[c] in encoders.keys():
                    oh = OneHotEncoder()
                    le = LabelEncoder()
                    le.fit(data_file.iloc[non_nan_indexes, c].values)

                    oh.fit(
                        le.transform(data_file.iloc[non_nan_indexes, c].values).reshape(
                            -1, 1
                        )
                    )
                    encoders[data_file.columns[c]] = (oh, le)
                c_encoder = encoders[data_file.columns[c]]

                encoded = c_encoder[0].transform(
                    c_encoder[1]
                    .transform(data_file.iloc[non_nan_indexes, c].values)
                    .reshape(-1, 1)
                )

                encoded = encoded.toarray()

                nan_data = np.empty((data_file.shape[0], encoded.shape[1]))
                nan_data[:, :] = np.nan
                encoded_column_names = [
                    data_file.columns[c] + "_" + str(i)
                    for i in range(0, encoded.shape[1])
                ]

                for i in range(0, non_nan_indexes.shape[0]):
                    nan_data[non_nan_indexes[i], :] = encoded[i, :]

                one_hot_column_map[data_file.columns[c]] = encoded_column_names

                for i, encoded_column in enumerate(encoded_column_names):
                    data_file[encoded_column] = nan_data[:, i]

        return data_file, one_hot_column_map, encoders

    def __translate_one_hot_encoded_columns(self, columns):

        translated_columns = columns.copy()
        for c in columns:
            if c in list(self.one_hot_column_map.keys()):
                translated_columns.remove(c)
                translated_columns += self.one_hot_column_map[c]

        return translated_columns

    def __propagate_dx(self, data_file: pd.DataFrame):
        data_file[self.DX] = data_file.groupby(self.PTID)[self.DX].ffill()
        data_file.loc[data_file[self.DX].isna(), self.DX] = data_file[
            data_file[self.DX].isna()
        ][self.DX_BL].values
        return data_file

    def __add_patient_columns(self):
        keys = [key for key in self.modality_columns.keys()]
        for key in keys:
            if key != "patient" and key != "adas13":
                self.modality_columns[key] = (
                    self.modality_columns[key] + self.modality_columns["patient"]
                )

    def __create_modality_combinations(self, max_size=2):
        modality_names = [
            key
            for key in self.modality_columns.keys()
            if (key != "patient") and (key != "adas13")
        ]
        if max_size is None or max_size > len(modality_names):
            max_size = len(modality_names)
        separator = "-"
        all_combinations = []

        for i in range(2, max_size + 1):
            all_combinations += list(itertools.combinations(modality_names, i))

        for c in all_combinations:
            combined_modality_columns = []
            for m in c:
                combined_modality_columns += self.modality_columns[m]

            combined_modality_columns = list(set(combined_modality_columns))

            new_combination = True
            new_modality_name = separator.join(c)
            # Ensure that the added combinatorial modality is not already presented with a different name
            # This only happens when overlapping modalities are defined in the modalities.yaml
            for k, v in self.modality_columns.items():
                if set(v) == set(combined_modality_columns):
                    new_combination = False
                    if self.verbosity:
                        print("%s already exists as %s" % (new_modality_name, k))
                    continue
            if new_combination:
                self.modality_columns[new_modality_name] = combined_modality_columns

    def use_challenge_modalities(self):
        filtered = {}
        if self.verbosity == 2:
            print("Replicating features utilized in the original TADPOLE challenge")
        for i, (modality, columns) in enumerate(self.modality_columns.items()):
            # Filter all modalities that contain word "apo4" except modality "apo4" and "patient-apo4"
            if "apo4" in modality and (
                modality != "apo4" or modality != "apo4-patient"
            ):
                continue
            # Filter all modalities that contain cognitive1 but do not contain cognitive_simple
            if ("cognitive1" in modality and ("cognitive_simple") not in modality) or (
                "cognitive_simple" in modality and "cognitive1" not in modality
            ):
                continue
            # ADAS13 and MMSE were merged with cognitive1.
            if modality == "cognitive_simple":
                continue
            filtered[modality] = columns
        self.modality_columns = filtered
        self.modality_names = self.get_modalities()

    def save_modality(self, save_folder):
        if self.verbosity > 1:
            print("Saving modalities")
        for modality in self.modality_columns.keys():
            column_names = self.modality_columns[modality]
            column_names.extend(
                [self.PTID, self.C_MONTH, self.DN[0], self.DN[1], self.EXAM_DATE]
            )
            if isinstance(self._df, vx.dataframe.DataFrame):
                data = self._df[
                    list(set(self._df.get_column_names()) & set(column_names))
                ]
            else:
                data = self._df[self._df.columns.intersection(column_names)]
            if self.backend == "vaex":
                data = data.to_pandas_df()

        data.to_csv(save_folder + modality + ".csv")

    def get_modalities(self):
        return [key for key in self.modality_columns.keys()]

    def getXY(
        self,
        ptids,
        modality,
        target=None,
        time_points=None,
        retrieve_meta=False,
        split=True,
        impute_ptids=[],
        include_target=False,
    ):

        value_columns = self.modality_columns[modality].copy()

        if self.AGE not in self.modality_columns[modality]:
            value_columns += [self.AGE]
        if include_target and target and not target in value_columns:
            value_columns += [target]
        selected_columns = value_columns.copy()
        selected_columns += [self.C_MONTH]
        if target and not target in selected_columns:
            selected_columns += [target]
        selected_columns += [self.PTID]

        measurements = self._df[self._df[self.PTID].isin(ptids)][
            selected_columns
        ].copy()

        if time_points is not None:
            measurements = measurements[measurements[self.C_MONTH].isin(time_points)]
        if target is not None:
            # If the only missing column is the target column, impute the missing target
            measurements[self.IMPUTED] = 0
            if len(impute_ptids) > 0:
                target_missing = measurements[
                    (measurements[target].isna())
                    & (measurements[value_columns].isna().sum(axis=1) <= 1)
                ]
                with pd.option_context("mode.chained_assignment", None):
                    measurements[measurements.index.isin(target_missing.index)][
                        self.IMPUTED
                    ] = 1
                if target_missing.shape[0] > 0:
                    imputer = KNNImputer(weights="distance", n_neighbors=5)
                    # The missing target will be imputed using the "patient" modality
                    impute_modality_columns = self.modality_columns[
                        self.DEFAULT_IMPUTE_MODALITY
                    ].copy()
                    impute_modality_columns += [target]
                    training_measurements = self._df[
                        self._df[self.PTID].isin(impute_ptids)
                    ][impute_modality_columns]
                    imputer.fit(training_measurements.values)
                    imputed = imputer.transform(
                        measurements[impute_modality_columns].values
                    )[:, len(impute_modality_columns) - 1]
                    measurements[target] = imputed.tolist()
            else:
                if isinstance(measurements, vx.dataframe.DataFrame):
                    measurements = measurements.dropmissing(column_names=[target])
                else:
                    measurements.replace(r"^\s*$", pd.NA, regex=True, inplace=True)
                    measurements = measurements[measurements[target].notnull()]

        measurements = measurements.dropna()
        measurements[self.IMPUTED] = measurements[self.IMPUTED].astype(int)
        value_columns += [self.IMPUTED]
        if not split:
            return measurements

        x_measurement = measurements[value_columns]
        y_measurements = []
        if target:
            y_measurements = measurements[target]

        if retrieve_meta:
            return (
                x_measurement,
                y_measurements,
                measurements[[self.C_MONTH, self.PTID, self.IMPUTED]],
            )
        else:
            return x_measurement, y_measurements

    def get_features(self, ptids, features):
        measurements = self._df[self._df[self.PTID].isin(ptids)]
        measurements = measurements[
            features + [self.PTID, self.C_MONTH, self.EXAM_DATE, self.RID]
        ]
        measurements = measurements.dropna()
        return measurements

    def has_modality(
        self,
        ptid,
        modality,
        time_points=None,
        target=None,
        nan_mask=[],
        predictable=False,
    ):

        expected_columns = self.modality_columns[modality].copy()
        # Missing target feature may be imputed if it missing from the modality.
        if target:
            if target in expected_columns:
                expected_columns.remove(target)
            expected_columns.append(target)
        data = self._df
        if len(nan_mask) > 0:
            data = self._df.copy()
            data[nan_mask] = np.nan

        if time_points:
            data = data[
                (data[self.PTID] == ptid) & (data[self.C_MONTH].isin(time_points))
            ]
        else:
            data = data[data[self.PTID] == ptid]

        data = data.sort_values(self.C_MONTH)
        if predictable and target:
            return data[expected_columns].iloc[1:, :].dropna().shape[0] > 0
        else:
            return data[expected_columns].dropna().shape[0] > 0

    def get_patient_modalities(self, ptid, time_points=None, target=None):
        return [
            modality
            for modality in self.get_modalities()
            if self.has_modality(ptid, modality, time_points=time_points, target=target)
        ]

    def get_ptids(self, min_time_points=1, target=None):

        columns = [self.PTID]
        if target:
            columns.append(target)
        if min_time_points == 1:
            ptids = self._df[columns]
        else:
            counts = self._df[self.PTID].value_counts()
            ptids = self._df[
                self._df[self.PTID].isin(counts.index[counts >= min_time_points])
            ]
        if target is not None:
            ptids = ptids.sort_values(self.C_MONTH)
            predictable = (
                ptids.loc[
                    ptids.groupby(self.PTID)[target]
                    .apply(lambda x: x.iloc[1:])
                    .index.get_level_values(1),
                    :,
                ]
                .groupby(self.PTID)[target]
                .apply(lambda x: x.isnull().all())
            )
            predictable = predictable[~predictable]
            ptids = ptids[ptids[self.PTID].isin(predictable.index)]
        return ptids[self.PTID].unique().tolist()

    def column_difference(self, df1: pd.DataFrame, df2: pd.DataFrame):
        df2_columns = []

        def extract_column(c):
            one_hot = re.search("([A-Z]*)(?=[_][0-9])", c)
            if one_hot is not None:
                return one_hot.group(0)
            else:
                return c

        for c in df2.columns:
            df2_columns.append(extract_column(c))
        df2_columns = list(set(df2_columns))
        difference = []
        for c in df1.columns:
            extracted = extract_column(c)
            if extracted not in df2_columns:
                difference.append(c)
        return difference

    def get_patient_time_points(self, ptid):
        return sorted(
            self._df[self._df[self.PTID].isin([ptid])][self.C_MONTH].values.tolist()
        )

    def distance_to_date(self, ptid: str, month: int, target_date: str):
        date_for_month = self._df[
            (self._df[TADPOLEData.PTID].isin([ptid]))
            & (self._df[TADPOLEData.C_MONTH].isin([month]))
        ][TADPOLEData.EXAM_DATE]
        if date_for_month.shape[0] > 0:
            date_for_month = date_for_month.values[0]
            distance = relativedelta(
                datetime.strptime(target_date, "%Y-%m-%d"),
                datetime.strptime(date_for_month, "%Y-%m-%d"),
            )
            return distance.years * 12 + distance.months
        else:
            return np.nan

    def rids_to_ptids(self, rids):

        rid_df: pd.DataFrame = pd.DataFrame(data=rids, columns=[self.RID])
        ptid_df: pd.DataFrame = self._df[[self.PTID, self.RID]]
        ptid_df = (
            ptid_df.merge(rid_df, left_on=self.RID, right_on=self.RID, how="inner")
            .groupby(self.PTID)
            .head(1)
        )
        return ptid_df[self.PTID].values.tolist()

    def save_dummy(self, file_name="dummy_data.csv", n_samples=300):

        dummy = self.df_raw.copy()

        for c in dummy.columns:
            dummy[c] = np.random.permutation(dummy[c].values)

        dummy = dummy[
            dummy[TADPOLEData.PTID].isin(dummy[TADPOLEData.PTID].unique()[0:n_samples])
        ]
        dummy.to_csv(file_name)
