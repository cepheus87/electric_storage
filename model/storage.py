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
        self._max_input_power = None  # in kWh
        self._max_output_power = None  # in kWh

        self._current_energy = 0
        self.used_energy = 0
        self.produced_energy = 0

    def set_parameters(self, **kwargs):
        """
        Function sets parameters of storage
        """
        self._min_capacity_perc = kwargs.get("min_capacity_perc")
        self._max_capacity_perc = kwargs.get("max_capacity_perc")
        self._max_input_power = kwargs.get("max_input_power")
        self._max_output_power = kwargs.get("max_output_power")

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

    def _use_capacity(self, used) -> float:
        """
        use battery capacity if needed
        :param used: consumed energy
        :return: energy still to consume after emptying storage
        """

        storage_used = min(used, self._max_output_power, self._current_energy)
        self._current_energy = self._current_energy - storage_used

        return used - storage_used

    def _recharge(self, produced) -> float:
        """
        Recharging battery
        :param produced: available energy
        :return: left energy after recharging
        """

        charged = min(produced, self._max_input_power, self.real_capacity - self._current_energy)
        self._current_energy = self._current_energy + charged

        return produced - charged

    def _update(self, row: pd.Series):
        """
        Update electric storage status per time interval
        :param row:
        """

        # flow:
        # use battery
        # recharge_battery to speed limit
        # balance

        to_consume = self._use_capacity(row["used"])
        surplus_energy = self._recharge(row["produced"])

        balanced_used = surplus_energy - to_consume

        if balanced_used < 0:
            self.used_energy += abs(balanced_used)
        else:
            self.produced_energy += balanced_used

    def process_data(self):
        """
        Simulate electric storage usage
        :param data:
        :return:
        """
        self.data.apply(self._update, axis=1)
