from datetime import datetime

def display_grocery_mapping(groceries):
    """Display mapping of grocery IDs and names."""
    print("\n--- Grocery ID - Name Mapping ---")
    for item in groceries:
        print(f"ID: {item['id']} - Name: {item['name']}")
    print("---------------------------------")

def get_product_name(groceries, product_id):
    """Utility to get product name from ID."""
    for item in groceries:
        if item['id'] == product_id:
            return item['name']
    return "Unknown"

def parse_date(date_str):
    """Parse date from DD/MM/YYYY format."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def search_by_date(transactions, groceries, search_date):
    """Search and display transactions by date (DD/MM/YYYY)."""
    results = [t for t in transactions if t['date'] == search_date]
    if not results:
        print(f"No transactions found on {search_date}.")
    else:
        print(f"\nTransactions on {search_date}:")
        print(f"{'Time':<12} | {'Product':<20} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t['id'])
            print(f"{t['time']:<12} | {name:<20} | {t['quantity']:<5} | {t['payment']:<8}")

def search_by_name(transactions, groceries, search_name):
    """Search and display transactions by product name (partial, case-insensitive)."""
    search_name = search_name.lower()
    matching_ids = [g['id'] for g in groceries if search_name in g['name'].lower()]
    
    results = [t for t in transactions if t['id'] in matching_ids]
    
    if not results:
        print(f"No transactions found for product matching '{search_name}'.")
    else:
        print(f"\nTransactions for products matching '{search_name}':")
        print(f"{'Date':<12} | {'Time':<12} | {'Product':<20} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t['id'])
            print(f"{t['date']:<12} | {t['time']:<12} | {name:<20} | {t['quantity']:<5} | {t['payment']:<8}")

def search_by_name_and_date(transactions, groceries, search_name, start_date, end_date):
    """Search by name and date range (DD/MM/YYYY)."""
    search_name = search_name.lower()
    matching_ids = [g['id'] for g in groceries if search_name in g['name'].lower()]
    
    try:
        start_dt = datetime.strptime(start_date, "%d/%m/%Y")
        end_dt = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        print("Error: Invalid date format. Use DD/MM/YYYY.")
        return

    results = []
    for t in transactions:
        t_dt = parse_date(t['date'])
        if t_dt and t['id'] in matching_ids and start_dt <= t_dt <= end_dt:
            results.append(t)
            
    if not results:
        print("No transactions found matching criteria.")
    else:
        print(f"\nTransactions for '{search_name}' from {start_date} to {end_date}:")
        print(f"{'Date':<12} | {'Time':<12} | {'Product':<20} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t['id'])
            print(f"{t['date']:<12} | {t['time']:<12} | {name:<20} | {t['quantity']:<5} | {t['payment']:<8}")

def update_grocery_details(groceries):
    """Change price or stock of an existing grocery (Manager only)."""
    display_grocery_mapping(groceries)
    g_id = input("Enter Grocery ID to update: ")
    product = next((g for g in groceries if g['id'] == g_id), None)
    
    if not product:
        print("Error: Grocery ID not found.")
        return
        
    print(f"Current details for {product['name']}: Price={product['price']}, Stock={product['stock']}")
    
    new_price = input("Enter new price (leave blank to keep current): ")
    new_stock = input("Enter new stock level (leave blank to keep current): ")
    
    try:
        if new_price:
            product['price'] = str(float(new_price))
        if new_stock:
            product['stock'] = str(int(new_stock))
        print("Product updated successfully.")
    except ValueError:
        print("Error: Invalid numerical value entered.")
