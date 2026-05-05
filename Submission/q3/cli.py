# cli.py - main program, run this from the terminal
# usage: python cli.py <transactions.csv> <groceries.csv>

import sys
import os

import database
import auth
import products
import transactions
import analytics


def setup():
    """load the csv files from command line args"""
    if len(sys.argv) != 3:
        print("Usage: python cli.py <transaction_file> <grocery_file>")
        print("  e.g. python cli.py data/transactions.csv data/groceries.csv")
        sys.exit(1)

    txn_path = sys.argv[1]
    groc_path = sys.argv[2]
    base = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.join(base, 'data', 'users.csv')

    database.initialize(groc_path, txn_path, users_path)
    print(f"Loaded {len(database.groceries_data)} products, {len(database.transactions_data)} transactions")


def login():
    print("\n=== Grocery Store System ===")
    while True:
        print("\n-- Login --")
        user = input("Username: ")
        pwd = input("Password: ")

        info = auth.authenticate(user, pwd)
        if info:
            print(f"\nWelcome {info['username']}! ({info['role']})")
            return info
        print("Wrong username or password, try again.")


def show_products():
    """prints product id/name mapping"""
    print(f"\n{'ID':<6} {'Name':<25} {'Price':>7} {'Stock':>6}")
    print("-" * 48)
    for p in products.get_all():
        print(f"{p['id']:<6} {p['name']:<25} ${p['price']:>6.2f} {p['stock']:>6}")
    print()


def print_txns(txns):
    if not txns:
        print("No transactions found.")
        return
    print(f"\n{'Date':<22} {'Product':<22} {'ID':<5} {'Qty':>4} {'Payment':>9}")
    print("-" * 65)
    for t in txns:
        print(f"{t['date']:<22} {t['product_name']:<22} {t['product_id']:<5} {t['qty']:>4} ${t['payment']:>8}")
    print(f"\n{len(txns)} records found")


# --- menu option functions ---

def do_sale():
    print("\n-- New Sale --")
    show_products()
    pid = input("Grocery ID: ")
    try:
        qty = int(input("Quantity: "))
        result = transactions.add_transaction(pid, qty)
        print(f"\nDone! {result['product_name']} x{result['qty']}")
        print(f"  Payment: ${result['payment']:.2f}")
        print(f"  Stock left: {result['remaining_stock']}")
    except ValueError as e:
        print(f"Error: {e}")


def do_add_product():
    print("\n-- Add New Product --")
    name = input("Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        p = products.add(name, price, stock)
        print(f"Added! ID: {p['id']}, {p['name']}, ${p['price']}, stock: {p['stock']}")
    except ValueError as e:
        print(f"Error: {e}")


def do_update_product():
    print("\n-- Update Product --")
    show_products()
    pid = input("Grocery ID to update: ")
    p = database.get_product_by_id(pid)
    if not p:
        print(f"Product '{pid}' not found")
        return

    print(f"Current: {p['name']} - ${p['price']:.2f}, stock: {p['stock']}")
    print("(press enter to skip)")

    price_in = input("New price: ")
    stock_in = input("New stock: ")

    price = float(price_in) if price_in.strip() else None
    stock = int(stock_in) if stock_in.strip() else None

    if price is None and stock is None:
        print("No changes.")
        return

    try:
        updated = products.update(pid, price=price, stock=stock)
        print(f"Updated: {updated['name']} - ${updated['price']:.2f}, stock: {updated['stock']}")
    except ValueError as e:
        print(f"Error: {e}")


def do_search_date():
    print("\n-- Search by Date --")
    s = input("Start date (YYYY-MM-DD): ")
    e = input("End date (YYYY-MM-DD): ")
    try:
        results = transactions.filter_by_date(s, e)
        print_txns(results)
    except ValueError as e2:
        print(f"Error: {e2}")


def do_search_name():
    print("\n-- Search by Product Name --")
    term = input("Search (partial ok): ")
    results = transactions.search_by_name(term)
    print_txns(results)


def do_search_both():
    print("\n-- Search by Name + Date --")
    term = input("Product name: ")
    s = input("Start date (YYYY-MM-DD): ")
    e = input("End date (YYYY-MM-DD): ")
    try:
        results = transactions.search_by_name_and_date(term, s, e)
        print_txns(results)
    except ValueError as e2:
        print(f"Error: {e2}")


def do_monthly_chart():
    print("\n-- Monthly Sales Chart --")
    s = input("Start month (YYYY-MM): ")
    e = input("End month (YYYY-MM): ")
    analytics.monthly_sales_chart(s, e)


def do_product_chart():
    print("\n-- Product Monthly Chart --")
    show_products()
    pid = input("Grocery ID: ")
    s = input("Start month (YYYY-MM): ")
    e = input("End month (YYYY-MM): ")
    analytics.product_monthly_chart(pid, s, e)


def do_bar_chart():
    print("\n-- Product Sales Bar Chart --")
    s = input("Start date (YYYY-MM-DD): ")
    e = input("End date (YYYY-MM-DD): ")
    analytics.product_bar_chart(s, e)


def do_pie_chart():
    print("\n-- Top 5 Products Pie Chart --")
    s = input("Start date (YYYY-MM-DD): ")
    e = input("End date (YYYY-MM-DD): ")
    analytics.top5_pie_chart(s, e)


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
            print(" 6. Change product details")
            print(" 7. Monthly sales chart")
            print(" 8. Product monthly sales chart")
            print(" 9. Product sales bar chart")
            print("10. Top 5 products pie chart")
        else:
            print(" 5. Monthly sales chart")
            print(" 6. Product monthly sales chart")
            print(" 7. Product sales bar chart")
            print(" 8. Top 5 products pie chart")

        print(" 0. Logout & Save")

        choice = input("\nChoice: ").strip()

        if choice == '0':
            database.flush_all()
            print("Data saved. Bye!")
            break
        elif choice == '1':
            do_sale()
        elif choice == '2':
            do_search_date()
        elif choice == '3':
            do_search_name()
        elif choice == '4':
            do_search_both()
        elif role == 'manager':
            if choice == '5': do_add_product()
            elif choice == '6': do_update_product()
            elif choice == '7': do_monthly_chart()
            elif choice == '8': do_product_chart()
            elif choice == '9': do_bar_chart()
            elif choice == '10': do_pie_chart()
            else: print("Invalid option.")
        else: # cashier
            if choice == '5': do_monthly_chart()
            elif choice == '6': do_product_chart()
            elif choice == '7': do_bar_chart()
            elif choice == '8': do_pie_chart()
            else: print("Invalid option.")


if __name__ == '__main__':
    setup()
    user = login()
    main_menu(user)
