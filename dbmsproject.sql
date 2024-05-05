create table customers(customer_id serial primary key,name varchar(100) not null,address varchar(100),
					   phone_no varchar(20) default null,birthday date);

create table tables (table_id serial primary key, capacity int, is_available boolean);

create table waiter(waiter_id serial primary key, waiter_name varchar(100) not null, waiter_tips int default null);

create table transactions(transaction_id serial primary key,amount numeric(10,2),payment_method varchar,
    time timestamp,tips numeric(10,2));

create table delivery(delivery_id serial primary key,delivery_status varchar,address varchar(100));

create table orders(order_id serial primary key,customer_id int,table_id int,deliv_id int,
	is_delivery bool not null,order_status varchar 
	check(order_status='Serving' or order_status='Served' or order_status='Preparing' or order_status is null),
	waiter_id int references waiter(waiter_id),transaction_id int references transactions(transaction_id),
	foreign key (customer_id) references customers(customer_id),
	foreign key (table_id) references tables(table_id),
	foreign key (deliv_id) references delivery(delivery_id),
	check ((deliv_id is null and not is_delivery) or (deliv_id is not null and is_delivery)),
	check ((is_delivery = false and table_id is null and order_status is null) or (is_delivery = true)));

create table reservation(reservation_id serial primary key,table_id int,customer_id int not null,date date,
    size int default null,foreign key (customer_id) references customers(customer_id),
    foreign key (table_id) references tables(table_id));

create table menu(menu_id serial primary key,item_name varchar(100),description varchar(255), price numeric(10,2));


-- Trigger to add delivery to orders table when added to delivery table
create or replace function add_delivery_to_orders()
returns trigger as $$
begin
    insert into orders(customer_id, is_delivery, deliv_id)
    values (null, true, new.delivery_id);
    return new;
end;
$$ language plpgsql;

create trigger add_delivery_trigger
before insert on delivery
for each row
execute procedure add_delivery_to_orders();

-- Trigger to update waiter tips when new transaction is added
create or replace function update_waiter_tips()
returns trigger as $$
begin
    update waiter
    set waiter_tips = waiter_tips + new.tips
    where waiter_id = new.waiter_id;
    return new;
end;
$$ language plpgsql;

create trigger update_waiter_tips_trigger
after insert on transactions
for each row
execute procedure update_waiter_tips();


--Backend
-- Function to remove delivery order from orders table when removed from delivery table
create or replace function remove_delivery_from_orders()
returns trigger as $$
begin
    delete from orders where deliv_id = old.delivery_id;
    return old;
end;
$$ language plpgsql;

-- Trigger to remove delivery order from orders table when removed from delivery table
create trigger remove_delivery_trigger
after delete on delivery
for each row
execute procedure remove_delivery_from_orders();

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

-- Function to get customer information by ID
create or replace function get_customer_info_by_id(customer_id int)
returns table (
    customer_name varchar(100),
    address varchar(100),
    phone_no varchar(20),
    birthday date,
    delivery_address varchar(100),
    order_item_name varchar(100),
    transaction_amount numeric(10,2),
    reservation_table_id int,
    reservation_date date
)
as $$
begin
    return query
    select 
        c.name,c.address,c.phone_no,c.birthday,d.address as delivery_address,o.item_name as order_item_name,
        t.amount as transaction_amount,r.table_id as reservation_table_id,r.date as reservation_date
    from 
        customers c
    left join orders o on c.customer_id = o.customer_id
    left join delivery d on c.customer_id = d.customer_id
    left join transactions t on c.customer_id = t.customer_id
    left join reservation r on c.customer_id = r.customer_id
    where 
        c.customer_id = get_customer_info_by_id.customer_id;
end;
$$ language plpgsql;




