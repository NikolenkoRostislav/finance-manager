import pandas as pd


class BaseLoader:
    def __init__(self, config):
        self.config = config

    def load(self, file_path) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement the load method.")

    def toFloat(self, value):
        try:
            return float(str(value).replace(',', '.'))
        except ValueError:
            return None