from smnsr.patients import AugmentedTADPOLEData, TADPOLEData
import pandas as pd
import numpy as np


class BaseModel:
    def __init__(self, data: AugmentedTADPOLEData):
        self.data: AugmentedTADPOLEData = data

    def _process_x(self, x):
        if isinstance(x, list):
            return x, []
        if isinstance(x, pd.DataFrame):
            assert TADPOLEData.RID in x.columns

            if TADPOLEData.PTID not in x.columns:
                x[TADPOLEData.PTID] = self.data.data.rids_to_ptids(x[TADPOLEData.RID])

            ptids = x[self.data.data.PTID].unique()
            valid_ptids = []

            nan_mask = self.data.data.column_difference(self.data.data._df, x)

            for ptid in ptids:
                if len(self.data.data.get_patient_modalities(ptid)) == 0:
                    print(
                        "Warning: Patient %s has zero valid modalities. Patient will be omitted."
                        % ptid
                    )
                else:
                    valid_ptids.append(ptid)
        return valid_ptids, nan_mask

    def _adjust_target_months(self, ptid, start_month, forecast_start_date, target):
        distance = self.data.data.distance_to_date(
            ptid, start_month, forecast_start_date
        )
        return [month + distance for month in target]

    def _create_forecast_definition(
        self, ptids, forecast_start, forecast_end, step_size=1
    ):

        if isinstance(ptids, pd.DataFrame):
            if ptids.shape[1] == 2 and set(
                [TADPOLEData.PTID, TADPOLEData.C_MONTH]
            ) == set(ptids.columns):
                return ptids, []

        x, nan_mask = self._process_x(ptids)
        prediction_definition = pd.DataFrame()
        ptid_list = []
        month_list = []

        for ptid in x:
            time_points = self.data.data.get_patient_time_points(ptid)
            d_start = self.data.data.distance_to_date(
                ptid, time_points[-1], forecast_start
            )
            d_end = self.data.data.distance_to_date(ptid, time_points[-1], forecast_end)
            n_steps = d_end - d_start
            month_list += [
                d_start + i for i in range(0, n_steps + step_size, step_size)
            ]
            ptid_list += [ptid for _ in range(0, n_steps + step_size, step_size)]

        prediction_definition[TADPOLEData.PTID] = ptid_list
        prediction_definition[TADPOLEData.C_MONTH] = month_list
        return prediction_definition, nan_mask
