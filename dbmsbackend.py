import psycopg2
from datetime import datetime

# Database connection parameters
DB_NAME = "dbmsproject"
DB_USER = "postgres"
DB_PASSWORD = "pgadmin4"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to establish a database connection
def connect():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
        return None
    
# Function to create a new customer
def create_customer():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            name = input("Enter customer name: ")
            address = input("Enter customer address: ")
            phone_no = input("Enter customer phone number (optional, press Enter to skip): ").strip() or None
            birthday = input("Enter customer birthday (YYYY-MM-DD): ")
            cursor.execute("INSERT INTO customers (name, address, phone_no, birthday) VALUES (%s, %s, %s, %s)",
                           (name, address, phone_no, birthday))
            conn.commit()
            print("Customer created successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while creating customer.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()


# Function to reserve a table
def reserve_table():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            table_id = int(input("Enter table ID to reserve: "))
            date = input("Enter reservation date (YYYY-MM-DD): ")
            cursor.execute("INSERT INTO reservation (customer_id, table_id, date) VALUES (%s, %s, %s)",
                           (customer_id, table_id, date))
            conn.commit()
            print("Table reserved successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while reserving the table.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to remove a table reservation
def remove_reservation():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            reservation_id = int(input("Enter reservation ID to remove: "))
            cursor.execute("DELETE FROM reservation WHERE reservation_id = %s", (reservation_id,))
            conn.commit()
            print("Table reservation removed successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while removing the reservation.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to make an order
def make_order():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            table_id = int(input("Enter table ID for the order: "))
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            time = datetime.now()
            cursor.execute("INSERT INTO orders (customer_id, table_id, item_name, quantity, time) VALUES (%s, %s, %s, %s, %s)",
                           (customer_id, table_id, item_name, quantity, time))
            conn.commit()
            print("Order placed successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while placing the order.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to remove an order
def remove_order():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            order_id = int(input("Enter order ID to remove: "))
            cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
            conn.commit()
            print("Order removed successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while removing the order.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to change order status
def change_order_status():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            order_id = int(input("Enter order ID to change status: "))
            new_status = input("Enter new status: ")
            cursor.execute("UPDATE orders SET order_status = %s WHERE order_id = %s", (new_status, order_id))
            conn.commit()
            print("Order status changed successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while changing order status.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to make a delivery order
def make_delivery_order():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            address = input("Enter delivery address: ")
            cursor.execute("INSERT INTO delivery (address) VALUES (%s) RETURNING delivery_id", (address,))
            delivery_id = cursor.fetchone()[0]
            print("Delivery order placed successfully. Delivery ID:", delivery_id)
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while placing delivery order.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to remove a delivery order
def remove_delivery_order():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            delivery_id = int(input("Enter delivery ID to remove: "))
            cursor.execute("DELETE FROM delivery WHERE delivery_id = %s", (delivery_id,))
            conn.commit()
            print("Delivery order removed successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while removing delivery order.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to change delivery status
def change_delivery_status():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            delivery_id = int(input("Enter delivery ID to change status: "))
            new_status = input("Enter new status: ")
            cursor.execute("UPDATE delivery SET delivery_status = %s WHERE delivery_id = %s", (new_status, delivery_id))
            conn.commit()
            print("Delivery status changed successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while changing delivery status.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to make a transaction
def make_transaction():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            amount = float(input("Enter transaction amount: "))
            payment_method = input("Enter payment method: ")
            time = datetime.now()
            tips = float(input("Enter tips amount (if any): "))
            cursor.execute("INSERT INTO transactions (amount, payment_method, time, tips) VALUES (%s, %s, %s, %s)",
                           (amount, payment_method, time, tips))
            conn.commit()
            print("Transaction recorded successfully.")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error occurred while recording the transaction.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()
                       
# Function to display customer information by ID
def display_customer_info_by_id():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            cursor.callproc("get_customer_info_by_id", (customer_id,))
            customer_info = cursor.fetchall()
            if not customer_info:
                print("No customer found with the given ID.")
                return
            print("\nCustomer Information:")
            for row in customer_info:
                print("Customer Name:", row[0])
                print("Address:", row[1])
                print("Phone Number:", row[2])
                print("Birthday:", row[3])
        except psycopg2.Error as e:
            print("Error occurred while fetching customer information.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()
            # Function to display transactions by customer ID
def display_transactions_by_customer_id():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            cursor.callproc("get_transactions_by_customer_id", (customer_id,))
            transactions = cursor.fetchall()
            if not transactions:
                print("No transactions found for the customer.")
                return
            print("\nTransactions for Customer ID:", customer_id)
            for transaction in transactions:
                print("Transaction ID:", transaction[0])
                print("Amount:", transaction[1])
                print("Payment Method:", transaction[2])
                print("Time:", transaction[3])
                print("Tips:", transaction[4])
        except psycopg2.Error as e:
            print("Error occurred while fetching transactions.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to display delivery information by customer ID
def display_delivery_by_customer_id():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            cursor.callproc("get_delivery_by_customer_id", (customer_id,))
            deliveries = cursor.fetchall()
            if not deliveries:
                print("No deliveries found for the customer.")
                return
            print("\nDeliveries for Customer ID:", customer_id)
            for delivery in deliveries:
                print("Delivery ID:", delivery[0])
                print("Delivery Status:", delivery[1])
                print("Address:", delivery[2])
        except psycopg2.Error as e:
            print("Error occurred while fetching deliveries.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to display reservations by customer ID
def display_reservations_by_customer_id():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            cursor.callproc("get_reservations_by_customer_id", (customer_id,))
            reservations = cursor.fetchall()
            if not reservations:
                print("No reservations found for the customer.")
                return
            print("\nReservations for Customer ID:", customer_id)
            for reservation in reservations:
                print("Reservation ID:", reservation[0])
                print("Table ID:", reservation[1])
                print("Date:", reservation[2])
                print("Size:", reservation[3])
        except psycopg2.Error as e:
            print("Error occurred while fetching reservations.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

# Function to display orders by customer ID
def display_orders_by_customer_id():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            customer_id = int(input("Enter customer ID: "))
            cursor.callproc("get_orders_by_customer_id", (customer_id,))
            orders = cursor.fetchall()
            if not orders:
                print("No orders found for the customer.")
                return
            print("\nOrders for Customer ID:", customer_id)
            for order in orders:
                print("Order ID:", order[0])
                print("Table ID:", order[1])
                print("Delivery ID:", order[2])
                print("Is Delivery:", order[3])
                print("Order Status:", order[4])
                print("Waiter ID:", order[5])
                print("Transaction ID:", order[6])
        except psycopg2.Error as e:
            print("Error occurred while fetching orders.")
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()


# Main function to provide options to the user
def main():
    while True:
        print("\nSelect an option:")
        print("1. Reserve a table")
        print("2. Remove table reservation")
        print("3. Make an order")
        print("4. Remove an order")
        print("5. Change order status")
        print("6. Make a delivery order")
        print("7. Remove a delivery order")
        print("8. Change delivery status")
        print("9. Make a transaction")
        print("0. Exit")
        print("A. Create a new customer")
        print("B. Display options")

        choice = input("Enter your choice: ")
        if choice == "1":   
            reserve_table()
        elif choice == "2":
            remove_reservation()
        elif choice == "3":
            make_order()
        elif choice == "4":
            remove_order()
        elif choice == "5":
            change_order_status()
        elif choice == "6":
            make_delivery_order()
        elif choice == "7":
            remove_delivery_order()
        elif choice == "8":
            change_delivery_status()
        elif choice == "9":
            make_transaction()
        elif choice.upper() == "A":
            create_customer()
        elif choice.upper() == "B":
            print("\nSelect an option to display:")
            print("1. Customer information")
            print("2. Transactions")
            print("3. Deliveries")
            print("4. Reservations")
            print("5. Orders")
            print("0. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                display_customer_info_by_id()
            elif choice == "2":
                display_transactions_by_customer_id()
            elif choice == "3":
                display_delivery_by_customer_id()
            elif choice == "4":
                display_reservations_by_customer_id()
            elif choice == "5":
                display_orders_by_customer_id()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
                
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
