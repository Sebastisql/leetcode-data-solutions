import pandas as pd

def trips_and_users(trips: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:

    valid_users = users[users['banned']=='No']['users_id']

    return (
        trips
        .loc[lambda x: x['request_at'].between('2013-10-01', '2013-10-03')]
        .loc[lambda x: (x['client_id'].isin(valid_users)) & (x['driver_id'].isin(valid_users))]
        .assign(
            cancel_mask=lambda x: x['status'].isin(['cancelled_by_driver', 'cancelled_by_client'])
        )
        .groupby(['request_at'], as_index=False)
        .agg(
            Cancellation_Rate=('cancel_mask', 'mean')
        )
        .rename(columns={
            'request_at': 'Day',
            'Cancellation_Rate': 'Cancellation Rate'
        })
        .round({
            'Cancellation Rate': 2
        })
    )