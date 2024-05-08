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

def create_delivery_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS delivery (
            delivery_id SERIAL PRIMARY KEY,
            customer_id INT,
            address VARCHAR(100),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """
    execute_query(create_table_query)

def insert_delivery(customer_id, address):
    insert_query = "INSERT INTO delivery (customer_id, address) VALUES (%s, %s)"
    execute_query(insert_query, (customer_id, address))

def view_delivery():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM delivery")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return col_names, rows

def update_delivery(delivery_id, customer_id, address):
    update_query = "UPDATE delivery SET customer_id = %s, address = %s WHERE delivery_id = %s"
    execute_query(update_query, (customer_id, address, delivery_id))

def delete_delivery(delivery_id):
    delete_query = "DELETE FROM delivery WHERE delivery_id = %s"
    execute_query(delete_query, (delivery_id,))

#UI
def main():
    st.title("Delivery Management")

    operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    if operation == "Create":
        st.subheader("Create Delivery")
        customer_id = st.number_input("Customer ID", min_value=1)
        address = st.text_input("Address")
        if st.button("Create Delivery"):
            insert_delivery(customer_id, address)
            st.success("Delivery created successfully!")

    elif operation == "Read":
        st.subheader("View Delivery")
        col_names, delivery_data = view_delivery()
        if delivery_data:
            st.write("Delivery Data:")
            for row in delivery_data:
                formatted_row = {col_names[i]: value for i, value in enumerate(row)}
                st.write(formatted_row)
        else:
            st.write("No deliveries found.")

    elif operation == "Update":
        st.subheader("Update Delivery")
        delivery_id = st.number_input("Delivery ID to update", min_value=1)
        customer_id = st.number_input("New Customer ID", min_value=1)
        address = st.text_input("New Address")
        if st.button("Update Delivery"):
            update_delivery(delivery_id, customer_id, address)
            st.success("Delivery updated successfully!")

    elif operation == "Delete":
        st.subheader("Delete Delivery")
        delivery_id = st.number_input("Delivery ID to delete", min_value=1)
        if st.button("Delete Delivery"):
            delete_delivery(delivery_id)
            st.success("Delivery deleted successfully!")

if __name__ == "__main__":
    main()
