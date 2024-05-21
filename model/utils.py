import pandas as pd


def preprocess_data(data_path):
    def _change_time(date: str) -> str:
        day = date.split(" ")[0]
        time = date.split(" ")[1]
        h = int(time.split(":")[0])
        return time.replace(time, f"{day} {h - 1}:59:59")

    df = pd.read_csv(data_path, sep=";")
    df = df.iloc[:, :-1]
    df.columns = ["date", "value_kWh", "type"]
    rename_types = {'pobór': "used", 'oddanie': "produced", 'pobrana po zbilansowaniu': "used_balanced",
                    'oddana po zbilansowaniu': "produced_balanced"}

    for k, val in rename_types.items():
        idxes = df[df["type"] == k].index
        df.loc[idxes, "type"] = val

    df["date"] = df["date"].apply(_change_time)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")

    return df
