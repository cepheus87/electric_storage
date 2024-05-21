import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", "-d", type=str, required=True)

    args = parser.parse_args()


if __name__ == "__main__":
    main()
