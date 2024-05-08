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

def create_reservations_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS reservation (
            reservation_id SERIAL PRIMARY KEY,
            table_id INT,
            customer_id INT NOT NULL,
            date DATE,
            size INT DEFAULT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (table_id) REFERENCES tables(table_id)
        )
    """
    execute_query(create_table_query)

def insert_reservation(table_id, customer_id, date, size):
    insert_query = "INSERT INTO reservation (table_id, customer_id, date, size) VALUES (%s, %s, %s, %s)"
    execute_query(insert_query, (table_id, customer_id, date, size))

def view_reservations():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservation")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return col_names, rows


def update_reservation(reservation_id, table_id, customer_id, date, size):
    update_query = "UPDATE reservation SET table_id = %s, customer_id = %s, date = %s, size = %s WHERE reservation_id = %s"
    execute_query(update_query, (table_id, customer_id, date, size, reservation_id))


def delete_reservation(reservation_id):
    delete_query = "DELETE FROM reservation WHERE reservation_id = %s"
    execute_query(delete_query, (reservation_id,))

#UI
def main():
    st.title("Reservations Management")

    operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    if operation == "Create":
        st.subheader("Create Reservation")
        table_id = st.number_input("Table ID", min_value=1)
        customer_id = st.number_input("Customer ID", min_value=1)
        date = st.date_input("Date")
        size = st.number_input("Size", min_value=1)
        if st.button("Create Reservation"):
            insert_reservation(table_id, customer_id, date, size)
            st.success("Reservation created successfully!")

    elif operation == "Read":
        st.subheader("View Reservations")
        col_names, reservations_data = view_reservations()
        if reservations_data:
            st.write("Reservations Data:")
            for row in reservations_data:
                formatted_row = {col_names[i]: value for i, value in enumerate(row)}
                st.write(formatted_row)
        else:
            st.write("No reservations found.")

    elif operation == "Update":
        st.subheader("Update Reservation")
        reservation_id = st.number_input("Reservation ID to update", min_value=1)
        table_id = st.number_input("New Table ID", min_value=1)
        customer_id = st.number_input("New Customer ID", min_value=1)
        date = st.date_input("New Date")
        size = st.number_input("New Size", min_value=1)
        if st.button("Update Reservation"):
            update_reservation(reservation_id, table_id, customer_id, date, size)
            st.success("Reservation updated successfully!")

    elif operation == "Delete":
        st.subheader("Delete Reservation")
        reservation_id = st.number_input("Reservation ID to delete", min_value=1)
        if st.button("Delete Reservation"):
            delete_reservation(reservation_id)
            st.success("Reservation deleted successfully!")

if __name__ == "__main__":
    main()
