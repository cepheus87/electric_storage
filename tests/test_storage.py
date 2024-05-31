import os
import pandas as pd
import pytest

from model.storage import Storage


@pytest.mark.parametrize("start_energy, row, expected", [
    # charging, no using
    (0, pd.Series({"used": 0, "produced": 1}), {"used_energy": 0, "produced_energy": 0, "storage_energy": 1}),
    (0, pd.Series({"used": 0, "produced": 2.5}), {"used_energy": 0, "produced_energy": 0, "storage_energy": 2.5}),
    (0, pd.Series({"used": 0, "produced": 3.5}), {"used_energy": 0, "produced_energy": 1, "storage_energy": 2.5}),
    (2, pd.Series({"used": 0, "produced": 3.5}), {"used_energy": 0, "produced_energy": 2, "storage_energy": 3.5}),
    (2, pd.Series({"used": 0, "produced": 2}), {"used_energy": 0, "produced_energy": 0.5, "storage_energy": 3.5}),
    # no charging, using
    (2, pd.Series({"used": 1, "produced": 0}), {"used_energy": 0, "produced_energy": 0, "storage_energy": 1}),
    (2, pd.Series({"used": 2, "produced": 0}), {"used_energy": 0, "produced_energy": 0, "storage_energy": 0}),
    (3, pd.Series({"used": 4, "produced": 0}), {"used_energy": 1.5, "produced_energy": 0, "storage_energy": 0.5}),
    (0, pd.Series({"used": 4, "produced": 0}), {"used_energy": 4, "produced_energy": 0, "storage_energy": 0}),
    # charging and using
    (0, pd.Series({"used": 1, "produced": 1}), {"used_energy": 1, "produced_energy": 0, "storage_energy": 1}),
    (1, pd.Series({"used": 1, "produced": 1}), {"used_energy": 0, "produced_energy": 0, "storage_energy": 1}),
    (1, pd.Series({"used": 2, "produced": 2}), {"used_energy": 1, "produced_energy": 0, "storage_energy": 2}),
    (2, pd.Series({"used": 3, "produced": 3}), {"used_energy": 0.5, "produced_energy": 0, "storage_energy": 2.5}),
    (3, pd.Series({"used": 3, "produced": 1}), {"used_energy": 0.5, "produced_energy": 0, "storage_energy": 1.5}),
    (3, pd.Series({"used": 3, "produced": 3}), {"used_energy": 0, "produced_energy": 0, "storage_energy": 3}),

])
def test_storage_update(start_energy, row, expected):

    data_path = os.path.join("assets", "Data_2024-05-01_2024-05-19.csv")

    params = {"min_capacity_perc": 20, "max_capacity_perc": 90, "max_input_power": 2.5, "max_output_power": 2.5}
    storage = Storage(data_path, 5)
    storage.set_parameters(**params)
    storage._current_energy = start_energy

    storage._update(row)

    assert storage.produced_energy == expected["produced_energy"]
    assert storage.used_energy == expected["used_energy"]
    assert storage._current_energy == expected["storage_energy"]

