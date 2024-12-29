import pandas as pd

transactions = pd.read_csv(
    "nft_transactions_2019_2021.csv",
    parse_dates = ["sales_datetime"]
)

# remove useless features
transactions.drop(
    ["asset.collection.short_description", "asset.permalink","payment_token.usd_price"],
    axis=1,
    inplace=True
)

# Sort by asset_id and transaction_date in descending order
transactions_sorted = transactions.sort_values(by=["asset.id", "sales_datetime"], ascending=[True, False])

# Identify the most recent collection name for each asset_id
most_recent_collection = (
    transactions_sorted.groupby("asset.id", as_index=False).first()[["asset.id", "asset.collection.name"]]
)

# Merge the most recent names back into the original dataframe
transactions = transactions.merge(most_recent_collection, on="asset.id", suffixes=("", "_most_recent"))

# Replace collection_name with the most recent name where necessary
transactions["asset.collection.name"] = transactions["asset.collection.name_most_recent"]
transactions.drop(columns=["asset.collection.name_most_recent"], inplace=True)


# Identify the most recent name for each asset_id
most_recent_name = (
    transactions_sorted.groupby("asset.id", as_index=False).first()[["asset.id", "asset.name"]]
)

# Merge the most recent names back into the original dataframe
transactions = transactions.merge(most_recent_name, on="asset.id", suffixes=("", "_most_recent"))

# Replace asset.name with the most recent name where necessary
transactions["asset.name"] = transactions["asset.name_most_recent"]
transactions.drop(columns=["asset.name_most_recent"], inplace=True)



# Fill nas, for string columns, using the value "Unknown"
string_columns = ["asset.name", "asset.collection.name", "payment_token.name", "seller.user.username"]
transactions[string_columns] = transactions[string_columns].fillna("Unknown")

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
