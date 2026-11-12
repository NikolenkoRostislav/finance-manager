# finance-manager

Budget tracker for Monobank, PrivatBank and cash exports. Loads, cleans and categorizes transactions, then writes CSV reports.

## Run

```bash
pip install -r requirements.txt
python -m budget_tracker --input data
```

Optional: `-m YYYY-MM` (e.g. `-m 2026-09`) to include analytics for one month.

Reports are written to `output/`.

## Package structure

```
budget_tracker/
├── __main__.py     # CLI entry point
├── config.py       # loads paths and config from the input folder
├── loaders/        # one loader per bank/source (monobank, privatbank, cash)
├── cleaning.py     # validates rows, collects rejected ones
├── categorizer.py  # assigns categories from rules
├── analytics.py    # totals by category and month
└── reports.py      # writes CSV reports
```

## Example output

`output/reports/spending_by_month.csv`:

```csv
date,total_expenses
2026-08,19377.99
2026-09,11284.86
```

`output/reports/2026/09/spending_by_category.csv`:

```csv
category,total_expenses
Інше,-5518.46
Дохід,36700.0
Кафе,-3771.80
Комунальні,-844.74
Продукти,-12336.71
Підписки,-762.58
Транспорт,-2180.84
```

Rows that could not be parsed go to `output/rejected_rows.csv`.
