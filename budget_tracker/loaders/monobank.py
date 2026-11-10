import pandas as pd

from .base import BaseLoader


class MonobankLoader(BaseLoader):
    def load(self, file_path) -> pd.DataFrame:
        with open(file_path, "r", encoding='cp1251') as f:
            df = pd.read_csv(f, sep=';')

        df_standardized = pd.DataFrame(columns=['date', 'description','amount_uah', 'currency', 'source', 'category'])
        df_standardized['date'] = pd.to_datetime(df['Дата i час операції'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
        df_standardized['description'] = df['Опис операції']
        df_standardized['amount_uah'] = df['Сума в валюті картки (UAH)'].apply(self.toFloat)
        df_standardized['currency'] = 'UAH'
        df_standardized['source'] = 'Monobank'

        return df_standardized
