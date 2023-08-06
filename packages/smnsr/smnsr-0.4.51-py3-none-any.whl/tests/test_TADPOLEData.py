import unittest
from smnsr.patients import TADPOLEData
import pandas as pd
import os
import shutil

MODALITY_PATH = "../smnsr/modalities/"
OUTPUT_PATH = "../output/"
TMP_PATH = "./tmp/"
TARGET = "ADAS13"
D3_FILE = "D3.csv"
TEST_PTID = "test_ptid"
DATA_FILE = MODALITY_PATH + "TADPOLE_D1_D2.csv"


class TestTADPOLEWrapper(unittest.TestCase):

    assert os.path.exists(
        DATA_FILE
    ), "TADPOLE_D1_D2.csv must be stored in the modality folder"
    _data = TADPOLEData(data=DATA_FILE, modality_path=MODALITY_PATH)

    def test_init_from_df(self):
        df = pd.read_csv(DATA_FILE)
        data = TADPOLEData(data=df, modality_path=MODALITY_PATH)
        self.assertTrue(len(data.get_ptids()) > 0)

    def test_save_modality(self):
        if not os.path.exists(TMP_PATH):
            os.mkdir(TMP_PATH)
        self._data.save_modality(TMP_PATH)
        self.assertTrue(os.path.exists(TMP_PATH))
        if os.path.exists(TMP_PATH):
            shutil.rmtree(TMP_PATH)

    def test_get_modalities(self):
        modalities = self._data.get_modalities()
        self.assertIsNotNone(modalities)
        self.assertTrue(len(modalities) > 0)

    #
    def test_get_xy(self):
        ptids = self._data.get_ptids()
        for modality in self._data.get_modalities():
            x, y = self._data.getXY(ptids, modality, TARGET)
            self.assertIsNotNone(x)
            self.assertIsNotNone(y)
            self.assertTrue(x.shape[0] > 0)
            self.assertTrue(y.shape[0] == x.shape[0])

    def test_get_ptids(self):
        ptids = self._data.get_ptids()
        self.assertIsNotNone(ptids)
        self.assertTrue(len(ptids) > 0)

    def __create_test_data(self):
        d3_data = pd.read_csv(MODALITY_PATH + D3_FILE)
        d3_data = d3_data.tail(1).copy()
        d3_data[TADPOLEData.PTID] = self._data.get_ptids()
        d3_data[TADPOLEData.C_MONTH] = 0
        return d3_data

    def test_distance_to_date(self):
        months = self._data.distance_to_date("011_S_0002", 0, "2015-09-08")
        self.assertEqual(120, months)
