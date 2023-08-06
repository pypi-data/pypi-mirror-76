from unittest import TestCase
from smnsr.patients import TADPOLEData, AugmentedTADPOLEData
import pathlib
import pickle
import bz2
import os

MODALITY_PATH = "../smnsr/modalities/"
OUTPUT_PATH = "../output/"
TMP_PATH = "./tmp/"
TARGET = "ADAS13"
PTIDS = ["011_S_0002", "011_S_0003", "011_S_0003", "011_S_0003", "011_S_0003"]
TEST_PTID = "test_ptid"
DATA_FILE = "TADPOLE_D1_D2.csv"


class TestAugmentedTADPOLEData(TestCase):

    assert os.path.exists(
        MODALITY_PATH + DATA_FILE
    ), "TADPOLE_D1_D2.csv must be stored in the modality folder"

    TS_FILE = "fold_0.p"
    MERGED_TS_FILE = OUTPUT_PATH + "merged_all.p"
    MODALITY = "patient"
    SAVE_PATH = OUTPUT_PATH + "merged_saved"

    GOOGLE_DRIVE_URL = (
        "https://drive.google.com/uc?id=1diTUWzctbl5MfpgoKBuGa-hvIXVgJcx7"
    )
    assert os.path.exists(
        MERGED_TS_FILE
    ), "A merged ts file must be provided for testing"

    _tadpole_data: TADPOLEData = TADPOLEData(
        modality_k=2,
        challenge_filter=True,
        data=MODALITY_PATH + DATA_FILE,
        modality_path=MODALITY_PATH,
    )
    _data: AugmentedTADPOLEData = AugmentedTADPOLEData(
        _tadpole_data, MERGED_TS_FILE, _tadpole_data.get_ptids()
    )

    def test_get_ptids(self):
        self.assertTrue(len(self._tadpole_data.get_ptids()) > 0)

    def test_get_modalities(self):
        self.assertTrue(len(self._tadpole_data.get_modalities()) > 0)

    def test_get_xy(self):
        x, y, t = self._data.getXY(
            ["135_S_5275"], modality=self.MODALITY, target=TARGET
        )
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertEqual(x.shape[0], y.shape[0])
        self.assertTrue(x.shape[0] > 0)

    def test_y(self):
        y = self._data.getY(["135_S_5275"], TARGET)
        self.assertIsNotNone(y)
        self.assertTrue(y.shape[0] > 0)

    def test_save(self):
        self._data.save(self.SAVE_PATH, overwrite=False)
        self.assertTrue(pathlib.Path(self.SAVE_PATH).exists())

        with bz2.BZ2File(self.SAVE_PATH, "rb") as file:
            merged = pickle.load(file)
            self.assertTrue(isinstance(merged, list) or isinstance(merged, tuple))
            self.assertTrue(merged[0] == "merged")
        pathlib.Path(self.SAVE_PATH).unlink()
        self.assertFalse(pathlib.Path(self.SAVE_PATH).exists())

    def test_load_merged_from_disk(self):
        self._data.save(self.SAVE_PATH, overwrite=False)
        self.assertTrue(pathlib.Path(self.SAVE_PATH).exists())
        data: AugmentedTADPOLEData = AugmentedTADPOLEData(
            self._tadpole_data, self.MERGED_TS_FILE, self._tadpole_data.get_ptids()
        )
        x, y, y = data.getXY(self._tadpole_data.get_ptids(), self.MODALITY, TARGET)
        self.assertTrue(x.shape[0] > 0)
        pathlib.Path(self.SAVE_PATH).unlink()
        self.assertFalse(pathlib.Path(self.SAVE_PATH).exists())

    def test_load_merged_from_google_drive(self):
        data: AugmentedTADPOLEData = AugmentedTADPOLEData(
            self._tadpole_data, self.GOOGLE_DRIVE_URL, self._tadpole_data.get_ptids()
        )
        x, y, y = data.getXY(self._tadpole_data.get_ptids(), self.MODALITY, TARGET)
        self.assertTrue(x.shape[0] > 0)
