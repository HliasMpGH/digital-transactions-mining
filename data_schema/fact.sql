create table [transactions_fact] (
    transaction_id bigint,
    seller_id int,
    asset_id int,
    buyer_id int,
    date_id int,
    token_id int,
    wei_price float,
    quantity int,
    primary key(transaction_id, seller_id, buyer_id, asset_id, date_id, token_id),
    foreign key (seller_id) references sellers_dim(seller_id),
    foreign key (asset_id) references assets_dim(asset_id),
    foreign key (date_id) references dates_dim(date_id),
    foreign key (token_id) references tokens_dim(token_id),
    foreign key (buyer_id) references buyers_dim(buyer_id)
)
