DROP TABLE USERS;
DROP TABLE ITEMS;
DROP TABLE ORDERS;
DROP TABLE ORDERS_ITEMS;

CREATE TABLE USERS (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT not null, 
    username varchar(1000)
);

CREATE TABLE Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT not null, 
    item_name nvarchar(1000),
    price Decimal(10,5)
);


CREATE TABLE ORDERS (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT not null,
    user_id bigint,
    order_date DATETIME
);


CREATE TABLE ORDERS_ITEMS (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT not null,
    item_id bigint
);
    
    


