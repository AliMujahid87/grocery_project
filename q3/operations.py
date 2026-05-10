from datetime import datetime

def display_grocery_mapping(groceries):
    """Display mapping of grocery IDs and names."""
    print("\n--- Grocery ID - Name Mapping ---")
    for item in groceries[1:]:
        print(f"ID: {item[0]} - Name: {item[1]}")
    print("---------------------------------")

def get_product_name(groceries, product_id):
    """Utility to get product name from ID."""
    for item in groceries[1:]:
        if item[0] == product_id:
            return item[1]
    return "Unknown"

def parse_date(date_str):
    """Parse date from DD/MM/YYYY format."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def search_by_date(transactions, groceries, search_date):
    """Search and display transactions by date (DD/MM/YYYY)."""
    results = [t for t in transactions[1:] if t[0] == search_date]
    if not results:
        print(f"No transactions found on {search_date}.")
    else:
        print(f"\nTransactions on {search_date}:")
        print(f"{'Time':<12} | {'Product':<20} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t[2])
            print(f"{t[1]:<12} | {name:<20} | {t[3]:<5} | {t[4]:<8}")

def search_by_name(transactions, groceries, search_name):
    """Search and display transactions by product name (partial, case-insensitive)."""
    search_name = search_name.lower()
    matching_ids = [g[0] for g in groceries[1:] if search_name in g[1].lower()]
    
    results = [t for t in transactions[1:] if t[2] in matching_ids]
    
    if not results:
        print(f"No transactions found for product matching '{search_name}'.")
    else:
        print(f"\nTransactions for products matching '{search_name}':")
        print(f"{'Date':<12} | {'Time':<12} | {'Product':<20} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t[2])
            print(f"{t[0]:<12} | {t[1]:<12} | {name:<20} | {t[3]:<5} | {t[4]:<8}")

def search_by_name_and_date(transactions, groceries, search_name, start_date, end_date):
    """Search by name and date range (DD/MM/YYYY)."""
    search_name = search_name.lower()
    matching_ids = [g[0] for g in groceries[1:] if search_name in g[1].lower()]
    
    try:
        start_dt = datetime.strptime(start_date, "%d/%m/%Y")
        end_dt = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        print("Error: Invalid date format. Use DD/MM/YYYY.")
        return

    results = []
    for t in transactions[1:]:
        t_dt = parse_date(t[0])
        if t_dt and t[2] in matching_ids and start_dt <= t_dt <= end_dt:
            results.append(t)
            
    if not results:
        print("No transactions found matching criteria.")
    else:
        print(f"\nTransactions for '{search_name}' from {start_date} to {end_date}:")
        print(f"{'Date':<12} | {'Time':<12} | {'Product':<20} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t[2])
            print(f"{t[0]:<12} | {t[1]:<12} | {name:<20} | {t[3]:<5} | {t[4]:<8}")

def update_grocery_details(groceries):
    """Change price or stock of an existing grocery (Manager only)."""
    display_grocery_mapping(groceries)
    g_id = input("Enter Grocery ID to update: ")
    product = next((g for g in groceries[1:] if g[0] == g_id), None)
    
    if not product:
        print("Error: Grocery ID not found.")
        return
        
    print(f"Current details for {product[1]}: Price={product[2]}, Stock={product[3]}")
    
    new_price = input("Enter new price (leave blank to keep current): ")
    new_stock = input("Enter new stock level (leave blank to keep current): ")
    
    try:
        if new_price:
            product[2] = str(float(new_price))
        if new_stock:
            product[3] = str(int(new_stock))
        print("Product updated successfully.")
    except ValueError:
        print("Error: Invalid numerical value entered.")
