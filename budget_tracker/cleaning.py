import pandas as pd


def clean(data):
    data_valid = data.dropna(subset=["date", "amount_uah", "description"])
    invalid_columns = data[~data.index.isin(data_valid.index)]
    invalid_columns["rejection_reason"] = "Invalid value"

    data_valid["description"] = data_valid["description"].str.strip()
    data_valid["description"] = data_valid["description"].str.lower()

    data_deduplicated = data_valid.drop_duplicates(subset=["date", "amount_uah", "description"])
    duplicated_columns = data_valid[~data_valid.index.isin(data_deduplicated.index)]
    duplicated_columns["rejection_reason"] = "Duplicate entry"
    data_deduplicated.reset_index(drop=True, inplace=True)

    return data_deduplicated, pd.concat([invalid_columns, duplicated_columns], ignore_index=True)