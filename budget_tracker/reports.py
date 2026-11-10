from pathlib import Path


def generate_reports(analytics_results, rejected_rows):
    spending_by_category, spending_by_month, spending_by_month_category = analytics_results

    reports_dir = Path('output/reports')
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    spending_by_category.to_csv(reports_dir / 'spending_by_category.csv', index=False)
    spending_by_month.to_csv(reports_dir / 'spending_by_month.csv', index=False)
    rejected_rows.to_csv(Path('output') / 'rejected_rows.csv', index=False)

    for _, row in spending_by_month_category.iterrows():
        month = row['date']

        output_dir = reports_dir / str(month.year) / f'{month.month:02d}'
        output_dir.mkdir(parents=True, exist_ok=True)

        monthly_report = row.drop('date').rename_axis('category').reset_index(name='total_expenses')

        monthly_report.to_csv(output_dir / 'spending_by_category.csv', index=False)

__all__ = ['generate_reports']