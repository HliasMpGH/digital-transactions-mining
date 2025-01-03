create table [sellers_dim] (
    seller_id int,
    seller_address varchar(100),
    seller_name nvarchar(100),
    primary key (seller_id)
)

create table [dates_dim] (
    date_id int,
    full_date date,
    day_name varchar(20),
    day_week_number int,
    day_month_number int,
    month_name varchar(20),
    month_number int,
    year_number int,
    hour_number int
    primary key (date_id)
)

create table [collections_dim] (
    collection_id int,
    collection_name nvarchar(200),
    primary key (collection_id)
)

create table [assets_dim] (
    asset_id int, -- id is already provided
    asset_name varchar(300),
    asset_category varchar(100),
    collection_id int,
    primary key (asset_id),
    foreign key (collection_id) references collections_dim(collection_id)
)

create table [tokens_dim] (
    token_id int,
    token_name varchar(100),
    primary key(token_id)
)

create table [buyers_dim] (
    buyer_id int,
    buyer_address varchar(100),
    primary key (buyer_id)
)
