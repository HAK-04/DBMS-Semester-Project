import streamlit as st
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="testdb",
    user="postgres",
    password="pgadmin4",
    host="localhost"
)

# Function to execute SQL queries
def execute_query(query, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()

# Function to create customers table
def create_customers_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address VARCHAR(100),
            phone_no VARCHAR(20),
            birthday DATE
        )
    """
    execute_query(create_table_query)

# Function to insert into customers table
def insert_customer(name, address, phone_no, birthday):
    insert_query = "INSERT INTO customers (name, address, phone_no, birthday) VALUES (%s, %s, %s, %s)"
    execute_query(insert_query, (name, address, phone_no, birthday))

# Function to view customers table
def view_customers():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return col_names, rows

# Function to update customers table
def update_customer(customer_id, name, address, phone_no, birthday):
    update_query = "UPDATE customers SET name = %s, address = %s, phone_no = %s, birthday = %s WHERE customer_id = %s"
    execute_query(update_query, (name, address, phone_no, birthday, customer_id))

# Function to delete from customers table
def delete_customer(customer_id):
    delete_query = "DELETE FROM customers WHERE customer_id = %s"
    execute_query(delete_query, (customer_id,))

# Streamlit UI
def main():
    st.title("Customer Management")

    # Topbar to select operation
    operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    if operation == "Create":
        st.subheader("Create Customer")
        name = st.text_input("Name")
        address = st.text_input("Address")
        phone_no = st.text_input("Phone Number")
        birthday = st.date_input("Birthday")
        if st.button("Create Customer"):
            insert_customer(name, address, phone_no, birthday)
            st.success("Customer created successfully!")

    elif operation == "Read":
        st.subheader("View Customers")
        col_names, customers_data = view_customers()
        if customers_data:
            st.write("Customers Data:")
            for row in customers_data:
                formatted_row = {col_names[i]: value for i, value in enumerate(row)}
                st.write(formatted_row)
        else:
            st.write("No customers found.")

    elif operation == "Update":
        st.subheader("Update Customer")
        customer_id = st.number_input("Customer ID to update", min_value=1)
        name = st.text_input("New Name")
        address = st.text_input("New Address")
        phone_no = st.text_input("New Phone Number")
        birthday = st.date_input("New Birthday")
        if st.button("Update Customer"):
            update_customer(customer_id, name, address, phone_no, birthday)
            st.success("Customer updated successfully!")

    elif operation == "Delete":
        st.subheader("Delete Customer")
        customer_id = st.number_input("Customer ID to delete", min_value=1)
        if st.button("Delete Customer"):
            delete_customer(customer_id)
            st.success("Customer deleted successfully!")

if __name__ == "__main__":
    main()
