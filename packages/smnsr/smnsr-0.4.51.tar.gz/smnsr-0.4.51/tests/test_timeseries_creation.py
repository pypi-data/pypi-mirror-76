import bz2
import pickle
import unittest
from smnsr.patients import TADPOLEData, AugmentedTADPOLEData
from smnsr.patients import create_features
from sklearn.model_selection import KFold
import psutil
import ray
import pandas as pd


class TestTimeseriesCreation(unittest.TestCase):

    MODALITIES = ["cognitive2"]
    OUTPUT_PATH = "../output/"
    MODALITY_PATH = "../smnsr/modalities/"
    DATA_FILE = MODALITY_PATH + "TADPOLE_D1_D2.csv"
    TARGET = "ADAS13"
    N_FOLDS = 10
    PATIENT_MODALITY = "patient"

    def test_create_features(self):
        data = TADPOLEData(
            data=self.DATA_FILE, modality_k=2, modality_path=self.MODALITY_PATH
        )
        ray.init(num_cpus=psutil.cpu_count(logical=False), ignore_reinit_error=True)
        ptids = data.get_ptids()
        timeseries_features, knn_models = create_features(
            data, ptids, [], modalities=self.MODALITIES
        )
        self.assertIsNotNone(timeseries_features)
        self.assertTrue(set(timeseries_features.keys()), set(self.MODALITIES))

    def test_precomputed_modality_for_ptid(self):
        tadpole_data = TADPOLEData(
            modality_k=8,
            data=self.DATA_FILE,
            challenge_filter=True,
            modality_path=self.MODALITY_PATH,
        )
        splitter = KFold(self.N_FOLDS, random_state=0, shuffle=True)
        # Patients with no predictable target value, i.e. patients with only baseline target value,
        # are not included in the augmented data.
        ptids = tadpole_data.get_ptids(min_time_points=2, target=self.TARGET)
        modalities = tadpole_data.get_modalities()

        for fold, (train_index, test_index) in enumerate(splitter.split(ptids)):
            with bz2.BZ2File(self.OUTPUT_PATH + "merged_%i.p" % fold, "rb") as file:
                merged = pickle.load(file)[1]

            with bz2.BZ2File(self.OUTPUT_PATH + "fold_%i.p" % fold, "rb") as file:
                split = pickle.load(file)

            train_ptids = [ptids[i] for i in train_index]
            test_ptids = [ptids[i] for i in test_index]
            aug_data = AugmentedTADPOLEData(
                tadpole_data, self.OUTPUT_PATH + "merged_%i.p" % fold, train_ptids
            )

            for ptid in test_ptids:

                self.assertTrue(
                    tadpole_data.has_modality(
                        ptid,
                        self.PATIENT_MODALITY,
                        target=self.TARGET,
                        predictable=True,
                    ),
                    "%s must always have %s modality" % (ptid, self.PATIENT_MODALITY),
                )

                has_valid_modality = False
                df_merged = merged["patient"][self.TARGET]
                df_fold = split["patient"][self.TARGET]

                self.assertTrue(
                    df_fold[df_fold[TADPOLEData.PTID].isin([ptid])].shape[0] > 0
                )
                self.assertTrue(
                    df_merged[df_merged[TADPOLEData.PTID].isin([ptid])].shape[0] > 0
                )

                for modality in modalities:
                    x, y, t = aug_data.getXY([ptid], modality, target=self.TARGET)
                    if x.shape[0] > 0:
                        has_valid_modality = True
                        break
                self.assertTrue(
                    has_valid_modality,
                    "%s must have at least single valid modality in fold %i"
                    % (ptid, fold),
                )
