import pandas as pd

from budget_tracker.config import Config


class BaseLoader:
    def __init__(self, config: Config):
        self.config = config

    def load(self, file_path) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement the load method.")

    def toFloat(self, value):
        try:
            return float(str(value).replace(',', '.'))
        except ValueError:
            return None

__all__ = ["BaseLoader"]