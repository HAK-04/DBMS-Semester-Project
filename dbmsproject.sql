create table customers(customer_id serial primary key,name varchar(100) not null,address varchar(100),
					   phone_no varchar(20) default null,birthday date);

create table tables (table_id serial primary key, capacity int, is_available boolean);

create table transactions(transaction_id serial primary key,amount numeric(10,2),payment_method varchar,
    date date,tips numeric(10,2));
alter table transactions add column customer_id int;
alter table transactions add constraint fk_customer_id foreign key (customer_id) references customers(customer_id); 

create table delivery(delivery_id serial primary key,delivery_status varchar,address varchar(100));
alter table delivery add column customer_id int;
alter table delivery drop column delivery_status;
alter table delivery add constraint fk_customer_id foreign key (customer_id) references customers(customer_id); 
select * from delivery;

create table orders(order_id serial primary key,customer_id int,table_id int,deliv_id int,
	is_delivery bool not null,order_status varchar 
	check(order_status='Served' or order_status='Preparing' or order_status='delivering'),
	item_name varchar, quantity int,
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
create or replace function get_customer_info()
returns table (
	c_id int,
    customer_name varchar(100),
    customer_address varchar(100),
    customer_phone_no varchar(20),
    customer_birthday date
)
as $$
begin
    return query
    select 
		customer_id as c_id,
        name as customer_name, 
        address as customer_address, 
        phone_no as customer_phone_no, 
        birthday as customer_birthday
    from 
        customers;
end;
$$ language plpgsql;

--Function to get transactions
create or replace function get_transactions()
returns table (
    t_id int,
    amountt numeric(10,2),
    p_method varchar,
    datee date,
    tipss numeric(10,2),
	c_id int
)
as $$
begin
    return query
    select 
        transaction_id as t_id, amount as amountt, payment_method as p_method, date as datee, tips as tipss, customer_id as c_id
    from 
        transactions;
end;
$$ language plpgsql;
--drop function get_transactions()

--Function to get delivery info
create or replace function get_delivery()
returns table (
    d_id int,
	c_id int,
    addresss varchar
)
as $$
begin
    return query
    select 
        delivery_id as d_id, customer_id as c_id, address as addresss
    from 
        delivery;
end;
$$ language plpgsql;
drop function get_delivery();

--Function to get reservations
create or replace function get_reservations()
returns table (
    r_id int,
	c_id int,
    t int,
    datee date,
    sizee int
)
as $$
begin
    return query
    select 
        reservation_id as r_id, customer_id as c_id, table_id as t_id, date as datee, size as sizee
    from 
        reservation;
end;
$$ language plpgsql;

--Function to get orders
create or replace function get_orders()
returns table (
    o_id int,
	c_id int,
    t_id int,
    d_id int,
    is_deliveryy bool,
    order_statuss varchar,
	item_namee varchar,
	quantityy int
)
as $$
begin
    return query
    select 
        order_id as o_id,customer_id as c_id, table_id as t_id, deliv_id as d_id, is_delivery as is_deliveryy,
		order_status as order_statuss, item_name as item_namee, quantity as quantityy
    from 
        orders;
end;
$$ language plpgsql;
drop function get_orders();
--Function to get Menu
create or replace function get_menu()
returns table (
    i_name varchar,
	descriptionn varchar,
	pricee numeric
)
as $$
begin
    return query
    select 
        item_name as i_name, description as descriptionn , price as pricee
    from 
        menu;
end;
$$ language plpgsql;
drop function get_menu();

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

-- Inserting test data into the transactions table
insert into transactions (amount, payment_method, date, tips,customer_id) values
    (50.00, 'Cash', '2024-05-01', 5.00,1),
    (75.00, 'Credit Card', '2024-05-02', 10.00,2),
    (100.00, 'Cash', '2024-05-03', 15.00,3);

-- Inserting test data into the delivery table
insert into delivery (customer_id, address) values
    (1,'321 Street'),
    (2,'XYZ Street'),
    (3,'123 Street');
--truncate table delivery cascade;  

-- Inserting test data into the orders table
insert into orders (customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity) values
    (1, 1, NULL, false, 'Served','Pizza',2),
    (2, 2, NULL, false, 'Preparing','Burger',1),
    (3, NULL, 2, true, 'Preparing','Salad',1);
select * from orders;

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
