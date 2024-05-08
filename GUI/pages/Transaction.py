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

def create_transactions_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            amount NUMERIC(10, 2),
            payment_method VARCHAR(100),
            date DATE,
            tips NUMERIC(10, 2),
            customer_id INT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """
    execute_query(create_table_query)

def insert_transaction(amount, payment_method, date, tips, customer_id):
    insert_query = "INSERT INTO transactions (amount, payment_method, date, tips, customer_id) VALUES (%s, %s, %s, %s, %s)"
    execute_query(insert_query, (amount, payment_method, date, tips, customer_id))


def view_transactions():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return col_names, rows


def update_transaction(transaction_id, amount, payment_method, date, tips, customer_id):
    update_query = "UPDATE transactions SET amount = %s, payment_method = %s, date = %s, tips = %s, customer_id = %s WHERE transaction_id = %s"
    execute_query(update_query, (amount, payment_method, date, tips, customer_id, transaction_id))

def delete_transaction(transaction_id):
    delete_query = "DELETE FROM transactions WHERE transaction_id = %s"
    execute_query(delete_query, (transaction_id,))

#UI
def main():
    st.title("Transactions Management")

    operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    if operation == "Create":
        st.subheader("Create Transaction")
        amount = st.number_input("Amount", min_value=0.0)
        payment_method = st.text_input("Payment Method")
        date = st.date_input("Date")
        tips = st.number_input("Tips", min_value=0.0)
        customer_id = st.number_input("Customer ID", min_value=1)
        if st.button("Create Transaction"):
            insert_transaction(amount, payment_method, date, tips, customer_id)
            st.success("Transaction created successfully!")

    elif operation == "Read":
        st.subheader("View Transactions")
        col_names, transactions_data = view_transactions()
        if transactions_data:
            st.write("Transactions Data:")
            for row in transactions_data:
                formatted_row = {col_names[i]: value for i, value in enumerate(row)}
                st.write(formatted_row)
        else:
            st.write("No transactions found.")

    elif operation == "Update":
        st.subheader("Update Transaction")
        transaction_id = st.number_input("Transaction ID to update", min_value=1)
        amount = st.number_input("New Amount", min_value=0.0)
        payment_method = st.text_input("New Payment Method")
        date = st.date_input("New Date")
        tips = st.number_input("New Tips", min_value=0.0)
        customer_id = st.number_input("New Customer ID", min_value=1)
        if st.button("Update Transaction"):
            update_transaction(transaction_id, amount, payment_method, date, tips, customer_id)
            st.success("Transaction updated successfully!")

    elif operation == "Delete":
        st.subheader("Delete Transaction")
        transaction_id = st.number_input("Transaction ID to delete", min_value=1)
        if st.button("Delete Transaction"):
            delete_transaction(transaction_id)
            st.success("Transaction deleted successfully!")

if __name__ == "__main__":
    main()
