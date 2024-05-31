import argparse

from model.storage import Storage


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", "-d", type=str, required=True)

    args = parser.parse_args()

    params = {"min_capacity_perc": 20, "max_capacity_perc": 90, "max_input_power": 2.5, "max_output_power": 2.5}

    storage = Storage(args.data_path, 5)
    storage.set_parameters(**params)

    storage.process_data()


if __name__ == "__main__":
    main()
