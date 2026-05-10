import csv
import sys
import os
from datetime import datetime

def load_data(filename):
    """Load data from a CSV file into a list of lists."""
    data = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return data

def save_data(filename, data):
    """Save a list of lists to a CSV file."""
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

def authenticate():
    """Authenticate user using users.csv."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, 'users.csv')
    users = load_data(users_file)
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        for user in users[1:]:
            # Index 0: username, 1: password, 2: type
            if user[0] == username and user[1] == password:
                print(f"Login successful! Welcome {username} ({user[2]}).")
                return user[2]
        
        print("Invalid username or password. Please try again.")

def display_grocery_mapping(groceries):
    """Display mapping of grocery IDs and names."""
    print("\n--- Grocery ID - Name Mapping ---")
    for item in groceries[1:]:
        print(f"ID: {item[0]} - Name: {item[1]}")
    print("---------------------------------")

def enter_sales_transaction(transactions, groceries):
    """Handle entering a new sales transaction."""
    display_grocery_mapping(groceries)
    
    product_id = input("Enter Grocery ID: ")
    
    # Check if ID exists
    product = next((item for item in groceries[1:] if item[0] == product_id), None)
    if not product:
        print("Error: Invalid Grocery ID.")
        return

    try:
        quantity = int(input(f"Enter quantity for {product[1]}: "))
        if quantity <= 0:
            print("Error: Quantity must be positive.")
            return
            
        current_stock = int(float(product[3]))
        if quantity > current_stock:
            print(f"Error: Not enough stock. Available: {current_stock}")
            return
            
        payment = float(input(f"Enter payment received (Price per item: {product[2]}): "))
        
        # Generate date and time separately as per transactions.csv
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        # Record transaction with correct order
        transactions.append([date_str, time_str, product_id, str(quantity), str(payment)])
        
        # Update stock
        product[3] = str(current_stock - quantity)
        
        print("Transaction added successfully.")
        
    except ValueError:
        print("Error: Invalid input for quantity or payment.")

def enter_new_grocery(groceries):
    """Handle entering a new grocery product (Manager only)."""
    # Auto-generate ID (numeric as per new data)
    ids = [int(g[0]) for g in groceries[1:] if g[0].isdigit()]
    new_id = str(max(ids) + 1 if ids else 1)

    print(f"Generating new Product ID: {new_id}")
    name = input("Enter Product Name: ")
    try:
        price = float(input("Enter Price: "))
        stock = int(input("Enter Initial Stock Level: "))
        
        groceries.append([new_id, name, str(price), str(stock)])
        print("New grocery product added successfully.")
    except ValueError:
        print("Error: Invalid input for price or stock.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <transaction_file> <grocery_file>")
        return

    trans_file = sys.argv[1]
    groc_file = sys.argv[2]

    transactions = load_data(trans_file)
    groceries = load_data(groc_file)

    role = authenticate()

    while True:
        print("\n--- Grocery Store Management Menu ---")
        print("1. Enter a sales transaction")
        if role == 'manager':
            print("2. Enter a new grocery product data")
        print("3. Logout")
        
        choice = input("Select an option: ")

        if choice == '1':
            enter_sales_transaction(transactions, groceries)
        elif choice == '2' and role == 'manager':
            enter_new_grocery(groceries)
        elif choice == '3':
            # Save data with correct format
            save_data(trans_file, transactions)
            save_data(groc_file, groceries)
            print("Data saved. Logging out...")
            break
        else:
            print("Invalid choice or unauthorized access.")

if __name__ == "__main__":
    main()
