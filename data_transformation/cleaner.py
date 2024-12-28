import pandas as pd

transactions = pd.read_csv(
    "nft_transactions_2019_2021.csv",
    parse_dates = ["sales_datetime"]
)

# remove useless features
transactions.drop(
    ["asset.collection.short_description", "asset.permalink"],
    axis=1,
    inplace=True
)

# remove Nans
transactions.dropna(inplace=True)

# create date features
transactions["day_name"] = transactions["sales_datetime"].dt.day_name()
transactions["day_of_week"] = transactions["sales_datetime"].dt.dayofweek
transactions["month_name"] = transactions["sales_datetime"].dt.month_name()
transactions["month_number"] = transactions["sales_datetime"].dt.month
transactions["year"] = transactions["sales_datetime"].dt.year
transactions["time"] = transactions["sales_datetime"].dt.time
transactions["hour"] = transactions["sales_datetime"].dt.hour
transactions["sales_datetime"] = transactions["sales_datetime"].dt.date # retain the date, remove the time

# make feature names more descriptive
transactions.rename({
    "sales_datetime": "full_date",
    "id": "transaction_id",
    "asset.id": "asset_id",
    "asset.name": "asset_name",
    "asset.collection.name": "collection_name",
    "total_price": "wei_price",
    "payment_token.name": "payment_token_name",
    "payment_token.usd_price": "usd_price",
    "asset.num_sales": "quantity",
    "seller.address": "seller_address",
    "seller.user.username": "seller_username",
    "winner_account.address": "buyer_address",
    "Category": "asset_category"
}, axis=1, inplace=True)

transactions.to_csv("nft_transactions_cleaned.csv", index=False)
