import pandas as pd

from .cash import CashLoader
from .monobank import MonobankLoader
from .privatbank import PrivatbankLoader


def load_data(config) -> pd.DataFrame:
    bank_exports = config.data_path / "bank_exports"
    dataframes = []

    for i in bank_exports.iterdir():
        if i.is_file():
            dataframes.append(load_data_from_file(config, i))
    return pd.concat(dataframes, ignore_index=True)

def choose_loader(config, file_path):
    if "monobank_" in file_path.name:
        return MonobankLoader(config)
    elif "privatbank_" in file_path.name:
        return PrivatbankLoader(config)
    elif "cash_" in file_path.name:
        return CashLoader(config)
    else:
        raise ValueError(f"Unsupported file format: {file_path.name}")

def load_data_from_file(config, file_path) -> pd.DataFrame:
    loader = choose_loader(config, file_path)
    return loader.load(file_path)

__all__ = ["load_data"]