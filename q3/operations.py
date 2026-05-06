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

def search_by_date(transactions, groceries, search_date):
    """Search and display transactions by date (YYYY-MM-DD)."""
    results = [t for t in transactions if t['date'].startswith(search_date)]
    if not results:
        print(f"No transactions found on {search_date}.")
    else:
        print(f"\nTransactions on {search_date}:")
        print(f"{'Date/Time':<20} | {'Product':<15} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t['product_id'])
            print(f"{t['date']:<20} | {name:<15} | {t['qty']:<5} | {t['payment']:<8}")

def search_by_name(transactions, groceries, search_name):
    """Search and display transactions by product name (partial, case-insensitive)."""
    search_name = search_name.lower()
    # Find matching product IDs
    matching_ids = [g['id'] for g in groceries if search_name in g['name'].lower()]
    
    results = [t for t in transactions if t['product_id'] in matching_ids]
    
    if not results:
        print(f"No transactions found for product matching '{search_name}'.")
    else:
        print(f"\nTransactions for products matching '{search_name}':")
        print(f"{'Date/Time':<20} | {'Product':<15} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t['product_id'])
            print(f"{t['date']:<20} | {name:<15} | {t['qty']:<5} | {t['payment']:<8}")

def search_by_name_and_date(transactions, groceries, search_name, start_date, end_date):
    """Search by name and date range (YYYY-MM-DD)."""
    search_name = search_name.lower()
    matching_ids = [g['id'] for g in groceries if search_name in g['name'].lower()]
    
    results = []
    for t in transactions:
        t_date = t['date'].split(' ')[0] # Get YYYY-MM-DD
        if t['product_id'] in matching_ids and start_date <= t_date <= end_date:
            results.append(t)
            
    if not results:
        print("No transactions found matching criteria.")
    else:
        print(f"\nTransactions for '{search_name}' from {start_date} to {end_date}:")
        print(f"{'Date/Time':<20} | {'Product':<15} | {'Qty':<5} | {'Payment':<8}")
        for t in results:
            name = get_product_name(groceries, t['product_id'])
            print(f"{t['date']:<20} | {name:<15} | {t['qty']:<5} | {t['payment']:<8}")

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
