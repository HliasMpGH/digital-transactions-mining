import pandas as pd

''' Read csv '''
transactions = pd.read_csv(
    "nft_transactions_2019_2021.csv",
    parse_dates = ["sales_datetime"]
)

''' Remove useless features'''
# remove useless features
transactions.drop(
    ["asset.collection.short_description", "asset.permalink", "payment_token.usd_price"],
    axis=1,
    inplace=True
)

''' Handle case of multiple collection names on same asset ids '''

# Sort by asset_id and transaction_date in descending order
transactions_sorted = transactions.sort_values(by=["asset.id", "sales_datetime"], ascending=[True, False])

# Identify the most recent collection name for each asset_id
most_recent_collection = (
    transactions_sorted.groupby("asset.id", as_index=False).first()[["asset.id", "asset.collection.name"]]
)

# Merge the most recent names back into the original dataframe
transactions = transactions.merge(most_recent_collection, on="asset.id",how='left', suffixes=("", "_most_recent"))

# Replace collection_name with the most recent name where necessary
transactions["asset.collection.name"] = transactions["asset.collection.name_most_recent"]
transactions.drop(columns=["asset.collection.name_most_recent"], inplace=True)


''' Handle case of multiple asset names on same assets ids '''

# Identify the most recent name for each asset_id
most_recent_name = (
    transactions_sorted.groupby("asset.id", as_index=False).first()[["asset.id", "asset.name"]]
)

# Merge the most recent names back into the original dataframe
transactions = transactions.merge(most_recent_name, on="asset.id",how='left', suffixes=("", "_most_recent"))

# Replace asset.name with the most recent name where necessary
transactions["asset.name"] = transactions["asset.name_most_recent"]
transactions.drop(columns=["asset.name_most_recent"], inplace=True)


''' Ensure one to one relationship between seller address and seller username '''

# Sort by seller address and transaction date in descending order
transactions_sorted = transactions.sort_values(by=["seller.address", "sales_datetime"], ascending=[True, False])

# Identify the most recent name for each seller address
most_recent_name = (
    transactions_sorted.groupby("seller.address", as_index=False).first()[["seller.address", "seller.user.username"]]
)

# Merge the most recent names back into the original dataframe
transactions = transactions.merge(most_recent_name, on="seller.address", how='left', suffixes=("", "_most_recent"))

# Replace seller.user.username with the most recent name where necessary
transactions["seller.user.username"] = transactions["seller.user.username_most_recent"]
transactions.drop(columns=["seller.user.username_most_recent"], inplace=True)

# Sort by username and transaction date in descending order
transactions_sorted = transactions.sort_values(by=["seller.user.username", "sales_datetime"], ascending=[True, False])

# Identify the most recent address for each valid username
most_recent_address = (
    transactions_sorted[transactions_sorted['seller.user.username'].notna()]  # Exclude NaN usernames
    .groupby("seller.user.username", as_index=False)
    .first()[["seller.user.username", "seller.address"]]
)

# Merge the most recent addresses back into the original dataframe
transactions = transactions.merge(most_recent_address, on="seller.user.username", how="left", suffixes=("", "_most_recent"))

# Replace seller.address with the most recent address where necessary
valid_mask = transactions['seller.user.username'].notna() & transactions['seller.address_most_recent'].notna()
transactions.loc[valid_mask, 'seller.address'] = transactions.loc[valid_mask, 'seller.address_most_recent']

# Drop the temporary column
transactions.drop(columns=["seller.address_most_recent"], inplace=True)



''' Handle case of multiple categories on same assets ids '''

# Identify the most recent category for each asset_id
most_recent_category = (
    transactions_sorted.groupby("asset.id", as_index=False).first()[["asset.id", "Category"]]
)

# Merge the most recent category back into the original dataframe
transactions = transactions.merge(most_recent_category, on="asset.id", how='left', suffixes=("", "_most_recent"))

# Replace Category with the most recent category where necessary
transactions["Category"] = transactions["Category_most_recent"]
transactions.drop(columns=["Category_most_recent"], inplace=True)

''' Remove transactions with quantity = 0 '''
transactions = transactions.loc[transactions['asset.num_sales'] > 0]

''' Fill missing values '''
# Fill nas, for string columns, using the value "Unknown"
string_columns = ["asset.name", "asset.collection.name", "payment_token.name", "seller.user.username"]
transactions[string_columns] = transactions[string_columns].fillna("Unknown")

''' Handle date columns'''
# create date features
transactions["day_name"] = transactions["sales_datetime"].dt.day_name()
transactions["day_of_week"] = transactions["sales_datetime"].dt.dayofweek
transactions["day_of_month"] = transactions["sales_datetime"].dt.day
transactions["month_name"] = transactions["sales_datetime"].dt.month_name()
transactions["month_number"] = transactions["sales_datetime"].dt.month
transactions["year"] = transactions["sales_datetime"].dt.year
transactions["time"] = transactions["sales_datetime"].dt.time
transactions["hour"] = transactions["sales_datetime"].dt.hour
transactions["sales_datetime"] = transactions["sales_datetime"].dt.date # retain the date, remove the time

''' Rename column names '''
# make feature names more descriptive
transactions.rename({
    "sales_datetime": "full_date",
    "id": "transaction_id",
    "asset.id": "asset_id",
    "asset.name": "asset_name",
    "asset.collection.name": "collection_name",
    "total_price": "wei_price",
    "payment_token.name": "payment_token_name",
    "asset.num_sales": "quantity",
    "seller.address": "seller_address",
    "seller.user.username": "seller_username",
    "winner_account.address": "buyer_address",
    "Category": "asset_category"
}, axis=1, inplace=True)

transactions.to_csv("nft_transactions_cleaned.csv", index=False)
