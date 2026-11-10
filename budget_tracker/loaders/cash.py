import pandas as pd


class CashLoader:
    def __init__(self, config):
        self.config = config

    def load(self, file_path) -> pd.DataFrame:
        return