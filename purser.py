import argparse


class Purser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('-q', '--query', help='word to search', type=str, required=True)
        self.parser.add_argument('-b', '--browser', help='browser name', type=str, choices=['chrome', 'firefox'], required=False)
        self.parser.add_argument('-n', '--number', help='Number of images to get', type=int, required=False)
        self.parser.add_argument('-d', '--save_dir', help='Save directory', type=str, required=False)

        self.args = self.parser.parse_args()

    def get_args(self) -> argparse.Namespace:
        return self.args
