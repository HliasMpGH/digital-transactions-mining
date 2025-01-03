import pandas as pd
import cleaner as _

transactions = pd.read_csv(
    "nft_transactions_cleaned.csv",
    dtype={"wei_price": float}
)

# define the features of the dimensions
sellers_columns = ["seller_address", "seller_username"]
dates_columns = [
    "full_date",
    "day_name",
    "day_of_week",
    "day_of_month",
    "month_name",
    "month_number",
    "year",
    "hour" # no need to include time
]
collections_columns = ["collection_name"]
assets_columns = ["asset_id", "asset_name", "asset_category", "collection_name"]
tokens_columns = ["payment_token_name"]
buyers_columns = ["buyer_address"]

fact_columns = [
    "transaction_id",
    "seller_address",
    "asset_id",
    "buyer_address",
    "full_date",
    "hour",
    "payment_token_name"
]
fact_measurements = ["wei_price", "quantity"]

# define the final dimensions
sellers_dim = transactions[sellers_columns].drop_duplicates(ignore_index=True)
dates_dim = transactions[dates_columns].drop_duplicates(ignore_index=True)
collections_dim = transactions[collections_columns].drop_duplicates(ignore_index=True)
assets_dim = transactions[assets_columns].drop_duplicates(ignore_index=True)
tokens_dim = transactions[tokens_columns].drop_duplicates(ignore_index=True)
buyers_dim = transactions[buyers_columns].drop_duplicates(ignore_index=True)
fact_table = transactions[fact_columns + fact_measurements]

# set manual PKs
sellers_dim["seller_id"] = sellers_dim.index + 1
dates_dim["date_id"] = dates_dim.index + 1
collections_dim["collection_id"] = collections_dim.index + 1
tokens_dim["token_id"] = tokens_dim.index + 1
buyers_dim["buyer_id"] = buyers_dim.index + 1
# assets already have an ID

# use address for the merge, as it belongs to only one user
fact_table = fact_table.merge(sellers_dim, how="left", on="seller_address")
fact_table = fact_table.merge(buyers_dim, how="left", on="buyer_address")
# in the current state of the data, we care only about date and hour level of detail
fact_table = fact_table.merge(dates_dim, how="left", on=["full_date", "hour"])
fact_table = fact_table.merge(tokens_dim, how="left", on="payment_token_name")
fact_table = fact_table.merge(assets_dim, how="left", on="asset_id")

# connect the tables with foreign keys
assets_dim = assets_dim.merge(collections_dim, how="left", on="collection_name") \
    .drop(["collection_name"], axis=1)

# remove left over features
fact_table.drop(
    sellers_columns +
    dates_columns +
    collections_columns +
    tokens_columns +
    buyers_columns +
    assets_columns[1:], # keep the asset_id
    axis=1,
    inplace=True
)

# remove commas on names as it may cause problems on SSIS
collections_dim["collection_name"] = collections_dim["collection_name"].str.replace(",", "")
assets_dim["asset_name"] = assets_dim["asset_name"].str.replace(",", "")

# write results
sellers_dim.to_csv("sellers_dim.csv", index=False)
dates_dim.to_csv("dates_dim.csv", index=False)
collections_dim.to_csv("collections_dim.csv", index=False)
assets_dim.to_csv("assets_dim.csv", index=False)
tokens_dim.to_csv("tokens_dim.csv", index=False)
buyers_dim.to_csv("buyers_dim.csv", index=False)
fact_table.to_csv("fact.csv", index=False)
