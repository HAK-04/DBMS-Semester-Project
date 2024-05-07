create table customers(customer_id serial primary key,name varchar(100) not null,address varchar(100),
					   phone_no varchar(20) default null,birthday date);

create table tables (table_id serial primary key, capacity int, is_available boolean);

create table waiter(waiter_id serial primary key, waiter_name varchar(100) not null, waiter_tips int default null);

create table transactions(transaction_id serial primary key,amount numeric(10,2),payment_method varchar,
    date date,tips numeric(10,2));

create table delivery(delivery_id serial primary key,delivery_status varchar,address varchar(100));

create table orders(order_id serial primary key,customer_id int,table_id int,deliv_id int,
	is_delivery bool not null,order_status varchar 
	check(order_status='Serving' or order_status='Served' or order_status='Preparing' or order_status is null),
	waiter_id int references waiter(waiter_id),transaction_id int references transactions(transaction_id),
	foreign key (customer_id) references customers(customer_id),
	foreign key (table_id) references tables(table_id),
	foreign key (deliv_id) references delivery(delivery_id));

create table reservation(reservation_id serial primary key,table_id int,customer_id int not null,date date,
    size int default null,foreign key (customer_id) references customers(customer_id),
    foreign key (table_id) references tables(table_id));

create table menu(menu_id serial primary key,item_name varchar(100),description varchar(255), price numeric(10,2));



--Backend


-- Function to update order status when changed
create or replace function update_order_status()
returns trigger as $$
begin
    update orders
    set order_status = new.status
    where order_id = new.order_id;
    return new;
end;
$$ language plpgsql;

-- Trigger to update order status when changed
create trigger update_order_status_trigger
after update on orders
for each row
execute procedure update_order_status();

--customer info
create or replace function get_customer_info_by_id(customer_id int)
returns table (
    customer_name varchar(100),
    customer_address varchar(100),
    customer_phone_no varchar(20),
    customer_birthday date
)
as $$
begin
    return query
    select 
        name as customer_name, 
        address as customer_address, 
        phone_no as customer_phone_no, 
        birthday as customer_birthday
    from 
        customers
    where 
        customers.customer_id = get_customer_info_by_id.customer_id;
end;
$$ language plpgsql;

--Function to get transactions
create or replace function get_transactions_by_customer_id(customer_id int)
returns table (
    transaction_id int,
    amount numeric(10,2),
    payment_method varchar,
    date timestamp,
    tips numeric(10,2)
)
as $$
begin
    return query
    select 
        transaction_id, amount, payment_method, time, tips
    from 
        transactions
    where 
        customer_id = get_transactions_by_customer_id.customer_id;
end;
$$ language plpgsql;

--Function to get delivery info
create or replace function get_delivery_by_customer_id(customer_id int)
returns table (
    delivery_id int,
    delivery_status varchar,
    address varchar(100)
)
as $$
begin
    return query
    select 
        delivery_id, delivery_status, address
    from 
        delivery
    where 
        customer_id = get_delivery_by_customer_id.customer_id;
end;
$$ language plpgsql;

--Function to get reservations
create or replace function get_reservations_by_customer_id(customer_id int)
returns table (
    reservation_id int,
    table_id int,
    date date,
    size int
)
as $$
begin
    return query
    select 
        reservation_id, table_id, date, size
    from 
        reservation
    where 
        customer_id = get_reservations_by_customer_id.customer_id;
end;
$$ language plpgsql;

--Function to get orders
create or replace function get_orders_by_customer_id(customer_id int)
returns table (
    order_id int,
    table_id int,
    deliv_id int,
    is_delivery bool,
    order_status varchar,
    waiter_id int,
    transaction_id int
)
as $$
begin
    return query
    select 
        order_id, table_id, deliv_id, is_delivery, order_status, waiter_id, transaction_id
    from 
        orders
    where 
        customer_id = get_orders_by_customer_id.customer_id;
end;
$$ language plpgsql;

-- Inserting test data into the customers table
insert into customers (name, address, phone_no, birthday) values
    ('Ali', '123 Main St', '123-456-7890', '2002-05-15'),
    ('Ammar', '456 Elm St', '987-654-3210', '1998-09-22'),
    ('Haroon', 'XYZ Street', NULL, '2001-12-10');

-- Inserting test data into the tables table
insert into tables (capacity, is_available) values
    (4, true),
    (2, true),
    (6, false);

-- Inserting test data into the waiter table
insert into waiter (waiter_name, waiter_tips) values
    ('Tom', 50),
    ('Anna', 30),
    ('Mike', 20);

-- Inserting test data into the transactions table
insert into transactions (amount, payment_method, date, tips) values
    (50.00, 'Cash', '2024-05-01', 5.00),
    (75.00, 'Credit Card', '2024-05-02', 10.00),
    (100.00, 'Cash', '2024-05-03', 15.00);

-- Inserting test data into the delivery table
insert into delivery values
    (1,'Delivered', '321 Street'),
    (2,'Pending', 'XYZ Street'),
    (3,'Delivered', '123 Street');

-- Inserting test data into the orders table
insert into orders (customer_id, table_id, deliv_id, is_delivery, order_status, waiter_id, transaction_id) values
    (1, 1, NULL, false, 'Served', 1, 1),
    (2, 2, NULL, false, 'Preparing', 2, 2),
    (3, NULL, 1, true, NULL, NULL, 3);


-- Inserting test data into the reservation table
insert into reservation (table_id, customer_id, date, size) values
    (1, 1, '2024-05-05', 4),
    (2, 2, '2024-05-06', 2),
    (3, 3, '2024-05-07', 6);

-- Inserting test data into the menu table
insert into menu (item_name, description, price) values
    ('Pizza', 'Margherita Pizza', 10.00),
    ('Burger', 'Beef Burger', 8.00),
    ('Salad', 'Caesar Salad', 6.00);
	
