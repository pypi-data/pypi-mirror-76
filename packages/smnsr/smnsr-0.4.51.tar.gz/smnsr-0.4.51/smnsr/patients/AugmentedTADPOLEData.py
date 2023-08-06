import pickle
import bz2
from smnsr.models import FROM, TO
from smnsr.patients import TADPOLEData
from pytictoc import TicToc
from pathlib import Path
import gdown
from tempfile import TemporaryDirectory
import os


class AugmentedTADPOLEData:

    FORECAST_DIST = "forecast_dist"
    Y = "y"
    TMP_FILE = "ts_tmp.p"

    def __init__(self, data, ts_data_file, train_ptids, verbosity=2, tmp_path=None):
        self.verbosity = verbosity
        self.train_ptids = train_ptids

        assert isinstance(data, TADPOLEData)

        if isinstance(data, TADPOLEData):
            self.data = data

        assert (
            isinstance(ts_data_file, str)
            or isinstance(ts_data_file, dict)
            or isinstance(ts_data_file, tuple)
            or isinstance(ts_data_file, list)
        )

        if isinstance(ts_data_file, str):
            tmp_dir = None
            if ts_data_file.startswith("https://"):
                tmp_dir: TemporaryDirectory = TemporaryDirectory()
                output = os.path.join(tmp_dir.name, self.TMP_FILE)
                gdown.download(ts_data_file, output, quiet=False)
                ts_data_file = output
            if verbosity == 2:
                print("Reading pre-calculated KNNSR data")
            with bz2.BZ2File(ts_data_file, "rb") as file:
                self.__process_knnsr_data(pickle.load(file))
            if verbosity == 2:
                print("Time series reading completed")
            if tmp_dir:
                tmp_dir.cleanup()
        else:
            self.__process_knnsr_data(ts_data_file)

    def __process_knnsr_data(self, knnsr_data):
        if isinstance(knnsr_data, dict):
            if self.verbosity == 2:
                print("Unmerged KNNSR data provided")
            self.__merge_knnr_data(knnsr_data)
        if isinstance(knnsr_data, tuple) or isinstance(knnsr_data, list):
            if self.verbosity == 2:
                print("Merged KNNSR data provided")
            self.views = knnsr_data[1]

    def __merge_knnr_data(self, knnsr_data):
        if self.verbosity == 2:
            print("Combining KNNSR data")
        self.views = {}
        ptids = self.data.get_ptids()
        tictoc = TicToc()
        tictoc.tic()
        self.valid_ptids = []
        for m in self.data.get_modalities():
            self.views[m] = {}
            for t in knnsr_data[m].keys():
                xy_measurement = self.data.getXY(
                    ptids, m, target=t, split=False, impute_ptids=self.train_ptids
                )
                modality_ts = knnsr_data[m][t]
                if not isinstance(modality_ts, self.data.backend.DataFrame):
                    modality_ts = self.data.backend.DataFrame(modality_ts)
                view = self.merge_view(xy_measurement, modality_ts)
                self.views[m][t] = view
                self.valid_ptids += view[TADPOLEData.PTID].values.tolist()
        if self.verbosity == 2:
            print("Mergin KNNSR data took %f" % tictoc.tocvalue())
        self.valid_ptids = list(set(self.valid_ptids))
        if self.verbosity == 2:
            print("%i patients in set" % len(self.valid_ptids))

    def merge_view(self, xy_measurement, modality_ts, offset=None):
        view = xy_measurement.merge(
            modality_ts,
            how="right",
            left_on=[self.data.PTID, self.data.C_MONTH],
            right_on=[self.data.PTID, FROM],
        )
        view[self.FORECAST_DIST] = view[TO] - view[FROM]
        return view

    def getXY(
        self,
        ptids,
        modality,
        target,
        start_time_points=None,
        target_time_points=None,
        knnsr_prediction=None,
    ):

        if knnsr_prediction is not None:
            view = knnsr_prediction
        else:
            view = self.views[modality][target]

        view = view[view[self.data.PTID].isin(ptids)]

        if start_time_points is not None:
            view = view[view[FROM].isin(start_time_points)]

        if target_time_points is not None:
            view = view[view[TO].isin(target_time_points)]

        x_columns = [
            c for c in view.columns if c not in [self.data.PTID, FROM, TO, self.Y]
        ]

        view = view.dropna().copy()
        if start_time_points is not None:
            view.loc[:, self.data.C_MONTH] = (
                view.loc[:, self.data.C_MONTH] - start_time_points
            )
            view.loc[:, FROM] = view.loc[:, FROM] - start_time_points
            view.loc[:, TO] = view.loc[:, TO] - start_time_points
        x = view[x_columns]
        y = view[self.Y]
        t = view[[FROM, TO]]

        return x, y, t

    def getY(self, ptids, target, drop_baseline=True):
        y = self.data.get_features(ptids, [target])
        counts = y[self.data.PTID].value_counts()
        y = y[y[self.data.PTID].isin(counts.index[counts >= 2])]
        if drop_baseline:
            y = y[y[TADPOLEData.C_MONTH] != 0]
        y.rename(columns={target: self.Y}, inplace=True)
        return y

    def get_ptids(self, training=False):
        if training:
            return self.valid_ptids
        return self.data.get_ptids()

    def get_modalities(self):
        return self.data.get_modalities()

    def save(self, output_path, overwrite=False):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if ~Path(output_path).exists() or overwrite:
            with bz2.BZ2File(output_path, "w") as file:
                pickle.dump(["merged", self.views], file)
                if self.verbosity == 2:
                    print("Saved merged %s" % output_path)
