import sys
import os
from datetime import datetime
import data_handler
import operations
import analytics

def authenticate():
    """Authenticate user using users.csv."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, 'users.csv')
    users = data_handler.load_csv(users_file)
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                print(f"Login successful! Welcome {username} ({user['type']}).")
                return user['type']
        
        print("Invalid username or password. Please try again.")

def enter_sales_transaction(transactions, groceries):
    """Handle entering a new sales transaction."""
    operations.display_grocery_mapping(groceries)
    
    product_id = input("Enter Grocery ID: ")
    product = next((item for item in groceries if item['id'] == product_id), None)
    if not product:
        print("Error: Invalid Grocery ID.")
        return

    try:
        quantity = int(input(f"Enter quantity for {product['name']}: "))
        if quantity <= 0:
            print("Error: Quantity must be positive.")
            return
            
        current_stock = int(float(product['stock']))
        if quantity > current_stock:
            print(f"Error: Not enough stock. Available: {current_stock}")
            return
            
        payment = float(input(f"Enter payment received (Price per item: {product['price']}): "))
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        transactions.append({
            'date': date_str,
            'time': time_str,
            'id': product_id,
            'quantity': str(quantity),
            'payment': str(payment)
        })
        product['stock'] = str(current_stock - quantity)
        print("Transaction added successfully.")
    except ValueError:
        print("Error: Invalid input.")

def enter_new_grocery(groceries):
    """Handle entering a new grocery product."""
    ids = [int(g['id']) for g in groceries if g['id'].isdigit()]
    new_id = str(max(ids) + 1 if ids else 1)

    print(f"New Product ID: {new_id}")
    name = input("Enter Product Name: ")
    try:
        price = float(input("Enter Price: "))
        stock = int(input("Enter Initial Stock Level: "))
        groceries.append({'id': new_id, 'name': name, 'price': str(price), 'stock': str(stock)})
        print("New product added.")
    except ValueError:
        print("Error: Invalid input.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <transaction_file> <grocery_file>")
        return

    trans_file = sys.argv[1]
    groc_file = sys.argv[2]

    transactions = data_handler.load_csv(trans_file)
    groceries = data_handler.load_csv(groc_file)

    role = authenticate()

    while True:
        print("\n--- Grocery Management System (Q3) ---")
        print("1. Enter a sales transaction")
        print("2. Search transactions")
        print("3. [Analysis] Monthly sales performance (Line Graph)")
        print("4. [Analysis] Product monthly performance (Line Graph)")
        print("5. [Analysis] Total sales per product (Bar Chart)")
        print("6. [Analysis] Top 5 products share (Pie Chart)")
        if role == 'manager':
            print("7. Enter a new grocery product")
            print("8. Change details of an existing grocery")
        print("0. Logout and Save")
        
        choice = input("Select an option: ")

        if choice == '1':
            enter_sales_transaction(transactions, groceries)
        elif choice == '2':
            print("\nSearch Options:")
            print("a. By Date")
            print("b. By Product Name")
            print("c. By Name and Date Range")
            sub_choice = input("Select search type: ").lower()
            if sub_choice == 'a':
                date = input("Enter date (DD/MM/YYYY): ")
                operations.search_by_date(transactions, groceries, date)
            elif sub_choice == 'b':
                name = input("Enter product name (partial): ")
                operations.search_by_name(transactions, groceries, name)
            elif sub_choice == 'c':
                name = input("Enter product name (partial): ")
                start = input("Enter start date (DD/MM/YYYY): ")
                end = input("Enter end date (DD/MM/YYYY): ")
                operations.search_by_name_and_date(transactions, groceries, name, start, end)
        elif choice == '3':
            start = input("Enter start month (YYYY-MM): ")
            end = input("Enter end month (YYYY-MM): ")
            analytics.display_monthly_line_graphs(transactions, start, end)
        elif choice == '4':
            operations.display_grocery_mapping(groceries)
            g_id = input("Enter Grocery ID: ")
            g_name = operations.get_product_name(groceries, g_id)
            start = input("Enter start month (YYYY-MM): ")
            end = input("Enter end month (YYYY-MM): ")
            analytics.display_monthly_line_graphs(transactions, start, end, product_name=g_name, product_id=g_id)
        elif choice == '5':
            start = input("Enter start date (DD/MM/YYYY): ")
            end = input("Enter end date (DD/MM/YYYY): ")
            analytics.display_total_sales_bar_chart(transactions, groceries, start, end)
        elif choice == '6':
            start = input("Enter start date (DD/MM/YYYY): ")
            end = input("Enter end date (DD/MM/YYYY): ")
            analytics.display_top_five_pie_chart(transactions, groceries, start, end)
        elif choice == '7' and role == 'manager':
            enter_new_grocery(groceries)
        elif choice == '8' and role == 'manager':
            operations.update_grocery_details(groceries)
        elif choice == '0':
            data_handler.save_csv(trans_file, transactions, ['date', 'time', 'id', 'quantity', 'payment'])
            data_handler.save_csv(groc_file, groceries, ['id', 'name', 'price', 'stock'])
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
