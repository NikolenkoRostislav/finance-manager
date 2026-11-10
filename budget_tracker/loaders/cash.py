import json

import pandas as pd

from .base import BaseLoader


class CashLoader(BaseLoader):
    def load(self, file_path) -> pd.DataFrame:
        data = {}
        with open(file_path, "r", encoding='utf-8') as f:
            data = json.load(f)

        df = pd.DataFrame.from_dict(data)
        df_standardized = pd.DataFrame(columns=['date', 'description','amount_uah', 'currency', 'source', 'category'])
        df_standardized['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
        df_standardized['description'] = df['note']
        df_standardized['amount_uah'] = df['amount'].apply(self.toFloat) * -1
        df_standardized['currency'] = 'UAH'
        df_standardized['source'] = 'Cash'
        df_standardized['category'] = df['category'].apply(lambda x: x if x in self.config.categories_rules else 'Інше')

        return df_standardized

__all__ = ['CashLoader']