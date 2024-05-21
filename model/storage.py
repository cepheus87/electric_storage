import pandas as pd

from model.utils import preprocess_data
import os


class Storage:

    def __init__(self, data_path: str, capacity_kWh: int):
        self.data_path = data_path
        self.data = preprocess_data(self.data_path)

        self.capacity = capacity_kWh
        self._min_capacity_perc = None
        self._max_capacity_perc = None

        self._current_energy = 0
        self.used_energy = 0
        self.produced_energy = 0

    def set_parameters(self, **kwargs):
        """
        Function sets parameters of storage
        """
        self._min_capacity_perc = kwargs.get("min_capacity_perc")
        self._max_capacity_perc = kwargs.get("max_capacity_perc")

    @property
    def data_path(self) -> str:
        return self._data_path

    @data_path.setter
    def data_path(self, value: str):
        os.path.exists(value)
        self._data_path = value

    @property
    def real_capacity(self):
        if all([self._min_capacity_perc, self._max_capacity_perc]):
            return (self._max_capacity_perc - self._min_capacity_perc) * self.capacity / 100
        else:
            raise RuntimeError("Storage parameters not set")

    def update(self, row: pd.Series):
        """
        Update electric storage status per time interval
        :param row:
        """
        pass

    def process_data(self):
        """
        Simulate electric storage usage
        :param data:
        :return:
        """
        self.data.apply(self.update, axis=1)
