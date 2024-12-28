create table [transactions_fact] (
    transactions_id int,
    seller_id int,
    asset_id int,
    date_id int,
    token_id int,
    wei_price float,
    usd_price float,
    quantity int,
    primary key(transactions_id, seller_id, asset_id, date_id, token_id)
    foreign key (seller_id) references seller_dim(seller_id)
    foreign key (asset_id) references assets_dim(asset_id)
    foreign key (date_id) references date_dim(date_id)
    foreign key (token_id) references tokens_dim(token_id)
)
