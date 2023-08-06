from unittest import TestCase
from smnsr.models import SMNSR
from smnsr.patients import AugmentedTADPOLEData, TADPOLEData
import pandas as pd
import pandas as pd
import numpy as np
import os


class TestSNSR(TestCase):

    MODALITY = "cognitive1"
    OUTPUT_PATH = "../output/"
    MODALITY_PATH = "../smnsr/modalities/"
    TARGET = "ADAS13"
    DATA_FILE = MODALITY_PATH + "TADPOLE_D1_D2.csv"
    D3_DATA_FILE = MODALITY_PATH + "D3.csv"
    TS_FILE = OUTPUT_PATH + "merged_all.p"
    PRE_CALCULATED_KNNSR = (
        "https://drive.google.com/uc?id=1diTUWzctbl5MfpgoKBuGa-hvIXVgJcx7"
    )

    assert os.path.exists(
        DATA_FILE
    ), "TADPOLE_D1_D2.csv must be stored in the modality folder"
    assert os.path.exists(D3_DATA_FILE), "D3.csv must be stored in the modality folder"
    assert os.path.exists(DATA_FILE), "Pre-merged ts data must be provided"
    tadpole_data = TADPOLEData(
        data=DATA_FILE, modality_k=8, challenge_filter=True, modality_path=MODALITY_PATH
    )
    data = AugmentedTADPOLEData(tadpole_data, TS_FILE, tadpole_data.get_ptids())
    FORECAST_STEP_SIZE = 6
    FORECAST_DISTANCE = 120
    D1_D2_FILE = "TADPOLE_D1_D2.csv"

    def __forecast_test(self, x, forecast_start="2018-01-01", data=None):

        if data is None:
            data = self.data

        model = SMNSR(data, training_cv_folds=2, mode="bypass_knnsr", forecast=True)
        model.fit(data.get_ptids())
        y_hat = model.predict(
            x.tail(10),
            self.TARGET,
            forecast_start=forecast_start,
            forecast_end="2022-12-01",
        )

        self.assertIsNotNone(y_hat)
        self.assertTrue(y_hat.shape[0] > 0)

    def test_forecast(self):
        x = self.data.get_ptids()[0:100]
        n_patients = len(x)
        model = SMNSR(
            self.data, training_cv_folds=2, mode="bypass_knnsr", forecast=True
        )
        model.fit(self.data.get_ptids())
        y_hat = model.predict(x, self.TARGET)

        self.assertIsNotNone(y_hat)
        self.assertTrue(y_hat.shape[0] > 0)

    def test_forecast_on_df(self):
        x: pd.DataFrame = pd.read_csv(
            self.MODALITY_PATH + self.D1_D2_FILE, low_memory=False
        )
        x = x.groupby(TADPOLEData.PTID).tail(1)
        self.__forecast_test(x)

    def test_forecast_on_df_to_date(self):
        x: pd.DataFrame = pd.read_csv(
            self.MODALITY_PATH + self.D1_D2_FILE, low_memory=False
        )
        x = x.groupby(TADPOLEData.PTID).tail(10)
        x = self.tadpole_data.df_raw
        self.__forecast_test(x, forecast_start="2020-12-01")

    def test_forecast_on_df_3(self):

        x: pd.DataFrame = pd.read_csv(self.D3_DATA_FILE, low_memory=False)
        x[TADPOLEData.PTID] = self.data.data.rids_to_ptids(x[TADPOLEData.RID])
        x = x.iloc[0:100, :]

        tadpole_data = TADPOLEData(
            data=self.DATA_FILE,
            modality_k=2,
            challenge_filter=False,
            modality_path=self.MODALITY_PATH,
        )
        data = AugmentedTADPOLEData(
            tadpole_data, self.TS_FILE, tadpole_data.get_ptids()
        )
        self.__forecast_test(x, data=data)

    def test_download_and_forecast_all(self):
        data = AugmentedTADPOLEData(
            self.tadpole_data, self.TS_FILE, self.tadpole_data.get_ptids()
        )

        model = SMNSR(
            data,
            training_cv_folds=2,
            verbosity=2,
            mode="bypass_knnsr",
            max_modalities=8,
            forecast=True,
        )
        model.fit(data.get_ptids())

        prediction = model.predict(self.tadpole_data.df_raw, target=self.TARGET)
        self.assertTrue(prediction.shape[0] > 0)
