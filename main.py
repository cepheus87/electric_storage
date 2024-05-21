import argparse

from model.storage import Storage


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", "-d", type=str, required=True)

    args = parser.parse_args()

    storage = Storage(args.data_path)
    storage


if __name__ == "__main__":
    main()
