import pandas as pd
from datetime import time

def find_golden_hour_customers(restaurant_orders: pd.DataFrame) -> pd.DataFrame:
    temp = restaurant_orders.copy()
    temp['order_timestamp'] = pd.to_datetime(temp['order_timestamp'], errors='coerce', dayfirst=True)
    return (
        temp
        .assign(
            peak_hours_mask=lambda x: 
                x['order_timestamp'].dt.time.between(time(11, 0), time(14, 0)) |
                x['order_timestamp'].dt.time.between(time(18, 0), time(21, 0))

        )
        .groupby(['customer_id'], as_index=False).agg(
            total_orders=('order_id', 'count'),
            rated_count=('order_rating', 'count'),
            average_rating=('order_rating', 'mean'),
            peak_hours=('peak_hours_mask', 'sum')
        )
        .assign(
            peak_hour_percentage=lambda x: x['peak_hours']/x['total_orders'],
            rated_percentage=lambda x: x['rated_count']/x['total_orders']
        )
        .query("total_orders >=3 and peak_hour_percentage >= 0.6 and average_rating >= 4 and rated_percentage >= 0.5")
        .loc[:, ['customer_id', 'total_orders', 'peak_hour_percentage', 'average_rating']]
        .round(
            {
                'average_rating': 2,
                'peak_hour_percentage': 2
            }
            )
        .assign(peak_hour_percentage=lambda x: x['peak_hour_percentage']*100)
        .sort_values(by=['average_rating', 'customer_id'], ascending=[False, False])
    )

