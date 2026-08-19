import pandas as pd

def find_loyal_customers(customer_transactions: pd.DataFrame) -> pd.DataFrame:
    return (
        customer_transactions
        .assign(
            transaction_date=lambda x: pd.to_datetime(x['transaction_date']),
            is_purchase=lambda x: x['transaction_type'].eq('purchase'),
            is_refund=lambda x: x['transaction_type'].eq('refund'),
        )
        .groupby(['customer_id'], as_index=False)
        .agg(
            purchase_count=('is_purchase', 'sum'),
            refund_count=('is_refund', 'sum'),
            max_date=('transaction_date', 'max'), 
            min_date=('transaction_date', 'min'), 
        )
        .query("purchase_count >= 3")
        .assign(
            active_days=lambda x: ((x['max_date']-x['min_date']).dt.days),
            total_relevant_count=lambda x: x['purchase_count'] + x['refund_count']
        )
        .query("active_days >= 30 and refund_count < 0.2 * total_relevant_count")
        [['customer_id']] 
        .sort_values(by=['customer_id'], ascending=[True], ignore_index=True)
    )