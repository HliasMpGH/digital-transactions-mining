import pandas as pd
import cleaner as _

transactions = pd.read_csv("nft_transactions_cleaned.csv")

# define the features of the dimensions
sellers_columns = ["seller_address", "seller_username"]
dates_columns = [
    "full_date",
    "day_name",
    "day_of_week",
    "month_name",
    "month_number",
    "year",
    "hour" # no need to include time
]
collections_columns = ["collection_name"]
tokens_columns = ["payment_token_name"]

# define the final dimensions
dates_dim = transactions[dates_columns]
tokens_dim = transactions[tokens_columns].drop_duplicates(ignore_index=True)

sorted_transactions = transactions.sort_values(
    by = ["full_date", "time"],
    ascending = True
)

# store only the most recent name of each collection
# we do that by making sure that the many-to-one relationship stays consistent
# with the asset_id and collection_id
collections_dim = sorted_transactions[["asset_id", "collection_name"]] \
    .drop_duplicates(["asset_id"], keep="last", ignore_index=True)

# store only the most recent name of each seller
sellers_dim = sorted_transactions[sellers_columns] \
    .drop_duplicates(["seller_address"], keep="last", ignore_index=True)


sellers_dim.to_csv("sellers_dim.csv", index=False)
dates_dim.to_csv("dates_dim.csv", index=False)
collections_dim.to_csv("collections_dim.csv", index=False)
tokens_dim.to_csv("tokens_dim.csv", index=False)

# To create the asset dimension, collection dim should be initialized in the db
# as it requires an auto-incremented foreign key
