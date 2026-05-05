# q1/cli.py - Basic Management System (Question 1)
import sys
import os

import database
import auth
import products
import transactions

def setup():
    if len(sys.argv) != 3:
        print("Usage: python cli.py <transaction_file> <grocery_file>")
        sys.exit(1)

    txn_path = sys.argv[1]
    groc_path = sys.argv[2]
    base = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.join(base, 'data', 'users.csv')

    database.initialize(groc_path, txn_path, users_path)
    print(f"Loaded {len(database.groceries_data)} products, {len(database.transactions_data)} transactions")

def login():
    print("\n=== Grocery Store System (Q1) ===")
    while True:
        print("\n-- Login --")
        user = input("Username: ")
        pwd = input("Password: ")
        info = auth.authenticate(user, pwd)
        if info:
            print(f"\nWelcome {info['username']}! ({info['role']})")
            return info
        print("Wrong username or password.")

def show_products():
    print(f"\n{'ID':<6} {'Name':<25} {'Price':>7} {'Stock':>6}")
    print("-" * 48)
    for p in products.get_all():
        print(f"{p['id']:<6} {p['name']:<25} ${p['price']:>6.2f} {p['stock']:>6}")

def main_menu(user_info):
    role = user_info['role']
    while True:
        print("\n" + "=" * 40)
        print(f" Menu ({user_info['username']} - {role})")
        print("=" * 40)
        print(" 1. Enter a sales transaction")
        if role == 'manager':
            print(" 2. Enter a new grocery product data")
        print(" 0. Logout & Save")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            print("\n-- New Sale --")
            show_products()
            pid = input("Grocery ID: ")
            try:
                qty = int(input("Quantity: "))
                result = transactions.add_transaction(pid, qty)
                print(f"\nDone! Sold {result['product_name']} x{result['qty']}")
                print(f"Total: ${result['payment']:.2f}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2' and role == 'manager':
            print("\n-- Add New Product --")
            name = input("Name: ")
            try:
                price = float(input("Price: "))
                stock = int(input("Stock: "))
                p = products.add(name, price, stock)
                print(f"Added! ID: {p['id']}, {p['name']}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '0':
            database.flush_all()
            print("Data saved. Bye!")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    setup()
    user = login()
    main_menu(user)
