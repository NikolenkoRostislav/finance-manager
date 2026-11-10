import pandas as pd
import json

class CashLoader:
    def __init__(self, config):
        self.config = config

    def load(self, file_path) -> pd.DataFrame:
        data ={}
        with open(file_path, "r", encoding='utf-8') as f:
            data = json.load(f)

        df = pd.DataFrame.from_dict(data)
        df_standardized = pd.DataFrame(columns=['date', 'description','amount_uah', 'currency', 'source', 'category'])
        df_standardized['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df_standardized['description'] = df['note']
        df_standardized['amount_uah'] = df['amount']
        df_standardized['currency'] = 'UAH'
        df_standardized['source'] = 'Cash'
        df_standardized['category'] = df['category'].apply(lambda x: x if x in self.config.categories_rules else 'Інше')
        return df_standardized