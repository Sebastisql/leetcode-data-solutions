import pandas as pd

def find_inventory_imbalance(stores: pd.DataFrame, inventory: pd.DataFrame) -> pd.DataFrame:
    return (
        inventory
        .assign(
            size_group=lambda x: x.groupby(['store_id'])['store_id'].transform('size')
        )
        .query("size_group >= 3")
        .drop(columns=['size_group'])
        .sort_values(by=['store_id', 'price'], ascending=[True, False])
        .groupby(['store_id'], as_index=False)
        .agg(
            most_exp_product=('product_name', 'first'),
            quantity_highest_price=('quantity', 'first'),
            cheapest_product=('product_name', 'last'),
            quantity_lowest_price=('quantity', 'last'),
        )
        .query("quantity_highest_price < quantity_lowest_price")
        .assign(
            imbalance_ratio=lambda x: x['quantity_lowest_price'] / x['quantity_highest_price']
        )
        .drop(columns=['quantity_lowest_price', 'quantity_highest_price'])
        .merge(stores, on='store_id', how='inner')
        .loc[:, ['store_id', 'store_name', 'location', 'most_exp_product', 'cheapest_product', 'imbalance_ratio']]
        .round({'imbalance_ratio': 2})
        .sort_values(by=['imbalance_ratio', 'store_name'], ascending=[False, True])
    )
