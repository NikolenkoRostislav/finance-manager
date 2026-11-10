import pandas as pd

from .base import BaseLoader


class PrivatbankLoader(BaseLoader):
    def load(self, file_path) -> pd.DataFrame:
        with open(file_path, "r", encoding='utf-8') as f:
            df = pd.read_csv(f, sep=',')

        df_standardized = pd.DataFrame(columns=['date', 'description','amount_uah', 'currency', 'source', 'category'])
        df_standardized['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
        df_standardized['description'] = df['description']
        df_standardized['amount_uah'] = df[['amount', 'currency']].apply(lambda x: 
            self.toFloat(x['amount']) 
            if x['currency'] == "UAH" 
            else self.config.exchange.usd_to_uah(self.toFloat(x['amount'])), 
            axis=1
        )
        df_standardized['currency'] = df['currency']
        df_standardized['source'] = 'Privatbank'

        return df_standardized
