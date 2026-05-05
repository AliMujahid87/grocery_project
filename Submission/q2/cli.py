# q2/cli.py - Search and Manipulation (Question 2)
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
    print("\n=== Grocery Store System (Q2) ===")
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

def print_txns(txns):
    if not txns:
        print("No transactions found.")
        return
    print(f"\n{'Date':<22} {'Product':<22} {'ID':<5} {'Qty':>4} {'Payment':>9}")
    print("-" * 65)
    for t in txns:
        print(f"{t['date']:<22} {t['product_name']:<22} {t['product_id']:<5} {t['qty']:>4} ${t['payment']:>8}")
    print(f"\n{len(txns)} records found")

def main_menu(user_info):
    role = user_info['role']
    while True:
        print("\n" + "=" * 40)
        print(f" Menu ({user_info['username']} - {role})")
        print("=" * 40)
        print(" 1. Enter a sales transaction")
        print(" 2. Search transactions by date")
        print(" 3. Search transactions by name")
        print(" 4. Search by name AND date range")
        
        if role == 'manager':
            print(" 5. Add new grocery product")
            print(" 6. Change details of an existing grocery product")
        
        print(" 0. Logout & Save")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            show_products()
            pid = input("Grocery ID: ")
            try:
                qty = int(input("Quantity: "))
                result = transactions.add_transaction(pid, qty)
                print(f"\nSuccess! Total: ${result['payment']:.2f}")
            except ValueError as e: print(f"Error: {e}")
        elif choice == '2':
            s = input("Start date (YYYY-MM-DD): ")
            e = input("End date (YYYY-MM-DD): ")
            try: print_txns(transactions.filter_by_date(s, e))
            except ValueError as e: print(f"Error: {e}")
        elif choice == '3':
            term = input("Search product name: ")
            print_txns(transactions.search_by_name(term))
        elif choice == '4':
            term = input("Product name: ")
            s = input("Start date (YYYY-MM-DD): ")
            e = input("End date (YYYY-MM-DD): ")
            try: print_txns(transactions.search_by_name_and_date(term, s, e))
            except ValueError as e: print(f"Error: {e}")
        elif choice == '5' and role == 'manager':
            name = input("Name: ")
            try:
                p = products.add(name, float(input("Price: ")), int(input("Stock: ")))
                print(f"Added! ID: {p['id']}")
            except ValueError as e: print(f"Error: {e}")
        elif choice == '6' and role == 'manager':
            show_products()
            pid = input("ID to update: ")
            try:
                p = products.update(pid, price=float(input("New price (skip with 0): ") or 0) or None, 
                                     stock=int(input("New stock (skip with -1): ") or -1) if True else None) # simple hack
                print("Updated!")
            except: print("Error updating.")
        elif choice == '0':
            database.flush_all()
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    setup()
    user = login()
    main_menu(user)
