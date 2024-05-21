from model.utils import preprocess_data
import pandas as pd
import os


class Storage:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = preprocess_data(self.data_path)

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, value):
        os.path.exists(value)
        self._data_path = value


