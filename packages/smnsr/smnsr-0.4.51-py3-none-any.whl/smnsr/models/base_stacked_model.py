from smnsr.patients import AugmentedTADPOLEData, TADPOLEData, create_features
from smnsr.models import BaseModel
import ray
import psutil


class BaseStackedModel(BaseModel):
    def __init__(self, data: AugmentedTADPOLEData):
        super().__init__(data)

    def __df_to_pdb(self, df, n_cpus=0):

        if n_cpus < 1:
            num_cpus = psutil.cpu_count(logical=False)

        ray.init(num_cpus=num_cpus)
        # Create a new patient database
        data = TADPOLEData(file=df)
        # Create augmented features for training
        ts_features, knn_models = create_features(
            data, data.get_ptids(), [], return_knn=True
        )
        return AugmentedTADPOLEData(data=data, time_series_data=ts_features), knn_models
