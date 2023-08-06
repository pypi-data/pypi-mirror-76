from unittest import TestCase
from smnsr.patients import TADPOLEData
from smnsr.models import KNNSR
import numpy as np

MODALITY_PATH = "../smnsr/modalities/"
DATA_FILE = MODALITY_PATH + "TADPOLE_D1_D2.csv"


class TestKNNSRModel(TestCase):

    data = TADPOLEData(
        data=DATA_FILE, challenge_filter=True, modality_k=2, modality_path=MODALITY_PATH
    )
    PTID = "011_S_0002"
    C_TIME = 0.0
    FORECAST_WINDOW = 6.0

    def test_fit(self):

        ptids = self.data.get_ptids()
        knn = KNNSR(self.data)
        knn.fit(ptids)
        self.assertTrue(knn.fitted)

    def test_predict(self):
        x = (
            np.array([[self.PTID, self.C_TIME]]),
            np.array([self.C_TIME + self.FORECAST_WINDOW]),
        )
        ptids = self.data.get_ptids()
        knn = KNNSR(self.data, modality="patient")
        knn.fit(ptids)
        prediction = knn.predict(x)

        self.assertIsNotNone(prediction)
