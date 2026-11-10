import pandas as pd


def generate_analytics(data, month):
    spending_by_category = data.groupby('category')['amount_uah'].sum().reset_index(name='total_expenses')

    spending_by_month = data.groupby(data['date'].dt.to_period('M'))['amount_uah'].sum().reset_index(name='total_expenses')

    spending_by_month_category = data.pivot_table(
        values='amount_uah',
        index=data['date'].dt.to_period('M'),
        columns='category',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    if month:
        monthly_report = (
            spending_by_month_category[spending_by_month_category['date'] == pd.Period(month, freq='M')]
            .drop(columns='date')
            .T
            .reset_index()
        )
        monthly_report.columns = ['category', 'total_expenses']

        print(monthly_report.to_string(index=False))

    return spending_by_category, spending_by_month, spending_by_month_category
