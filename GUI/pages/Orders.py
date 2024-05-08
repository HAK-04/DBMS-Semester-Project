import streamlit as st
import psycopg2

conn = psycopg2.connect(
    dbname="testdb",
    user="postgres",
    password="pgadmin4",
    host="localhost"
)

def execute_query(query, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()

def create_orders_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INT,
            table_id INT,
            deliv_id INT,
            is_delivery BOOLEAN NOT NULL,
            order_status VARCHAR(100) CHECK (order_status IN ('Served', 'Preparing', 'Delivering')),
            item_name VARCHAR(100),
            quantity INT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (table_id) REFERENCES tables(table_id),
            FOREIGN KEY (deliv_id) REFERENCES delivery(delivery_id)
        )
    """
    execute_query(create_table_query)


def insert_order(customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity):
    insert_query = "INSERT INTO orders (customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    execute_query(insert_query, (customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity))

# Function to view ord
def view_orders():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return col_names, rows


def update_order(order_id, customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity):
    update_query = "UPDATE orders SET customer_id = %s, table_id = %s, deliv_id = %s, is_delivery = %s, order_status = %s, item_name = %s, quantity = %s WHERE order_id = %s"
    execute_query(update_query, (customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity, order_id))


def delete_order(order_id):
    delete_query = "DELETE FROM orders WHERE order_id = %s"
    execute_query(delete_query, (order_id,))

#UI
def main():
    st.title("Orders Management")

    operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    if operation == "Create":
        st.subheader("Create Order")
        customer_id = st.number_input("Customer ID", min_value=1)
        table_id = st.number_input("Table ID", min_value=1)
        deliv_id = st.number_input("Delivery ID (optional)", min_value=1, value=None, step=1)
        is_delivery = st.checkbox("Is Delivery?")
        order_status = st.selectbox("Order Status", ("Served", "Preparing", "Delivering"))
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1)
        if st.button("Create Order"):
            insert_order(customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity)
            st.success("Order created successfully!")

    elif operation == "Read":
        st.subheader("View Orders")
        col_names, orders_data = view_orders()
        if orders_data:
            st.write("Orders Data:")
            for row in orders_data:
                formatted_row = {col_names[i]: value for i, value in enumerate(row)}
                st.write(formatted_row)
        else:
            st.write("No orders found.")

    elif operation == "Update":
        st.subheader("Update Order")
        order_id = st.number_input("Order ID to update", min_value=1)
        customer_id = st.number_input("New Customer ID", min_value=1)
        table_id = st.number_input("New Table ID", min_value=1)
        deliv_id = st.number_input("New Delivery ID (optional)", min_value=1, value=None, step=1)
        is_delivery = st.checkbox("Is Delivery?")
        order_status = st.selectbox("New Order Status", ("Served", "Preparing", "Delivering"))
        item_name = st.text_input("New Item Name")
        quantity = st.number_input("New Quantity", min_value=1)
        if st.button("Update Order"):
            update_order(order_id, customer_id, table_id, deliv_id, is_delivery, order_status, item_name, quantity)
            st.success("Order updated successfully!")

    elif operation == "Delete":
        st.subheader("Delete Order")
        order_id = st.number_input("Order ID to delete", min_value=1)
        if st.button("Delete Order"):
            delete_order(order_id)
            st.success("Order deleted successfully!")

if __name__ == "__main__":
    main()
