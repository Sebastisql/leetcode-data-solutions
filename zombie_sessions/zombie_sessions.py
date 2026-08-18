import pandas as pd
import numpy as np

def find_zombie_sessions(app_events: pd.DataFrame) -> pd.DataFrame:
    purchase_session = app_events.loc[app_events['event_type'] == 'purchase', 'session_id'].unique()
    return (
        app_events
        .query("session_id not in @purchase_session")
        .assign(
            event_timestamp=lambda x: pd.to_datetime(x['event_timestamp']),
            scroll_mask=lambda x: x['event_type'].eq('scroll'),
            click_mask=lambda x: x['event_type'].eq('click'),
        )
        .groupby(['user_id', 'session_id'], as_index=False, sort=False) #czy kolejność grupowania w tym przyapdku ma znaczenie, jeśli nie korzystam z indeksów?
        .agg(
            scroll_count=('scroll_mask', 'sum'),
            click_count=('click_mask', 'sum'),
            latest_date=('event_timestamp', 'max'),
            first_date=('event_timestamp', 'min'),
        )
        .query("scroll_count >= 5")
        .assign(
            session_duration_minutes=lambda x: (x['latest_date']-x['first_date']).dt.total_seconds()/60,
            click_to_scroll_ratio=lambda x: x['click_count']/x['scroll_count']
        )
        .query("session_duration_minutes > 30 and click_to_scroll_ratio < 0.2")
        .loc[:, ['session_id', 'user_id', 'session_duration_minutes', 'scroll_count']]
        .sort_values(by=['scroll_count', 'session_id'], ascending=[False, True])
    )
