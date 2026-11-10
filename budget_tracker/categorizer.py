import pandas as pd


def categorize(data, config):
    data['category'] = data[['description', 'category']].apply(lambda x: get_category(x, config.categories_rules), axis=1)
    return data

def get_category(row, rules):
    if pd.notna(row['category']):
        return row['category']

    for category, keywords in rules.items():
        if any(keyword.lower().strip() in row['description'] for keyword in keywords):
            return category

    return 'Інше'

__all__ = ['categorize']