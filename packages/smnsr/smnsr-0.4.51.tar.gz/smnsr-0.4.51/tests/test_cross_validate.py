from unittest import TestCase
from smnsr.patients import TADPOLEData, AugmentedTADPOLEData
from smnsr.cross_validate import perform_cv, parse_args, evaluate_predictions
from sklearn.model_selection import KFold
import pickle


class Test(TestCase):
    FOLDS = 2
    TARGET = "ADAS13"
    MODALITY_PATH = "../smnsr/modalities/"
    OUTPUT_PATH = "../output/"
    MODALITY_K = 2
    CV_RESULT_FILE = "cv_result.p"
    N_FOLDS = 10
    DATA_FILE = MODALITY_PATH + "TADPOLE_D1_D2.csv"

    CLI_ARGS = [
        "--folds",
        str(FOLDS),
        "--target",
        TARGET,
        "--modality_path",
        MODALITY_PATH,
        "--precomputed_path",
        OUTPUT_PATH,
        "--bl_forecast",
        "--precomputed",
        "--mode",
        "bypass_knnsr",
        "--modality_k",
        str(MODALITY_K),
        "--output_path",
        OUTPUT_PATH,
    ]

    def test_parse_args(self):
        args = parse_args(self.CLI_ARGS)
        self.assertEqual(args.folds, self.FOLDS)
        self.assertEqual(args.target, self.TARGET)
        self.assertEqual(args.precompute_path, self.OUTPUT_PATH)
        self.assertEqual(args.modality_path, self.MODALITY_PATH)
        self.assertTrue(args.bl_forecast)
        self.assertTrue(args.precomputed)

    def test_perform_cv(self):
        results = perform_cv(parse_args(self.CLI_ARGS))
        self.assertIsNotNone(results)

    def test_evaluate_predictions(self):
        tadpole_data = TADPOLEData(
            data=self.DATA_FILE, modality_k=2, modality_path=self.MODALITY_PATH
        )
        cv_results = pickle.load(open(self.OUTPUT_PATH + self.CV_RESULT_FILE, "rb"))
        evaluate_predictions(cv_results, tadpole_data)
        self.assertTrue(True)
