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

def create_menu_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS menu (
            menu_id SERIAL PRIMARY KEY,
            item_name VARCHAR(100),
            description VARCHAR(255),
            price NUMERIC(10, 2)
        )
    """
    execute_query(create_table_query)

def insert_menu(item_name, description, price):
    insert_query = "INSERT INTO menu (item_name, description, price) VALUES (%s, %s, %s)"
    execute_query(insert_query, (item_name, description, price))

def view_menu():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    return col_names, rows

def update_menu(menu_id, item_name, description, price):
    update_query = "UPDATE menu SET item_name = %s, description = %s, price = %s WHERE menu_id = %s"
    execute_query(update_query, (item_name, description, price, menu_id))

def delete_menu(menu_id):
    delete_query = "DELETE FROM menu WHERE menu_id = %s"
    execute_query(delete_query, (menu_id,))

#UI
def main():
    st.title("Menu Management")


    operation = st.sidebar.radio("Select Operation", ("Create", "Read", "Update", "Delete"))

    if operation == "Create":
        st.subheader("Create Menu Item")
        item_name = st.text_input("Item Name")
        description = st.text_input("Description")
        price = st.number_input("Price", min_value=0.0)
        if st.button("Create Menu Item"):
            insert_menu(item_name, description, price)
            st.success("Menu item created successfully!")

    elif operation == "Read":
        st.subheader("View Menu")
        col_names, menu_data = view_menu()
        if menu_data:
            st.write("Menu Data:")
            for row in menu_data:
                formatted_row = {col_names[i]: value for i, value in enumerate(row)}
                st.write(formatted_row)
        else:
            st.write("No menu items found.")

    elif operation == "Update":
        st.subheader("Update Menu Item")
        menu_id = st.number_input("Menu Item ID to update", min_value=1)
        item_name = st.text_input("New Item Name")
        description = st.text_input("New Description")
        price = st.number_input("New Price", min_value=0.0)
        if st.button("Update Menu Item"):
            update_menu(menu_id, item_name, description, price)
            st.success("Menu item updated successfully!")

    elif operation == "Delete":
        st.subheader("Delete Menu Item")
        menu_id = st.number_input("Menu Item ID to delete", min_value=1)
        if st.button("Delete Menu Item"):
            delete_menu(menu_id)
            st.success("Menu item deleted successfully!")

if __name__ == "__main__":
    main()
