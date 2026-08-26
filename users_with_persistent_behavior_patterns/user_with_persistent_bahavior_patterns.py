import pandas as pd

def find_behaviorally_stable_users(activity: pd.DataFrame) -> pd.DataFrame:
    return (
        activity
        .drop_duplicates(subset=['user_id', 'action_date'], keep=False)
        .assign(
            action_date=lambda x: pd.to_datetime(x['action_date']),
            rn=lambda x: x.groupby(['user_id', 'action'])['action_date'].rank(method='first', ascending=True),
            island_group_id=lambda x: x['action_date']-pd.to_timedelta(x['rn'], unit='d')
        )
        .groupby(['user_id', 'action', 'island_group_id'], as_index=False)
        .agg(
            streak_length=('user_id', 'size'),
            start_date=('action_date', 'min'),
            end_date=('action_date', 'max'),
        )
        .drop(columns=['island_group_id'])
        .query("streak_length >= 5")
        .sort_values(by=['streak_length', 'user_id', 'start_date'], ascending=[False, True, False])
        .drop_duplicates(subset=['user_id'], keep='first')
        .reset_index(drop=True)
    )
