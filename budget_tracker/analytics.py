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
        print(spending_by_month_category[spending_by_month_category['date'] == month])

    return spending_by_category, spending_by_month, spending_by_month_category
