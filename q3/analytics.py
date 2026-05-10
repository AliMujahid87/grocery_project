import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def get_monthly_data(transactions, start_month, end_month, product_id=None):
    """Process transactions to get monthly sales values and counts."""
    # start_month/end_month format: YYYY-MM
    months = []
    # Generate list of months between start and end
    try:
        start_dt = datetime.strptime(start_month, "%Y-%m")
        end_dt = datetime.strptime(end_month, "%Y-%m")
    except ValueError:
        print("Error: Invalid month format. Use YYYY-MM.")
        return [], [], []
    
    current_dt = start_dt
    while current_dt <= end_dt:
        months.append(current_dt.strftime("%Y-%m"))
        # Increment month
        if current_dt.month == 12:
            current_dt = current_dt.replace(year=current_dt.year + 1, month=1)
        else:
            current_dt = current_dt.replace(month=current_dt.month + 1)
            
    sales_values = {m: 0.0 for m in months}
    sales_counts = {m: 0 for m in months}
    
    for t in transactions[1:]:
        # Transactions date format: DD/MM/YYYY
        try:
            t_dt = datetime.strptime(t[0], "%d/%m/%Y")
            t_month = t_dt.strftime("%Y-%m")
            if t_month in months:
                if product_id is None or t[2] == product_id:
                    sales_values[t_month] += float(t[4])
                    sales_counts[t_month] += 1
        except (ValueError, KeyError):
            continue
                
    return months, [sales_values[m] for m in months], [sales_counts[m] for m in months]

def display_monthly_line_graphs(transactions, start_month, end_month, product_name=None, product_id=None):
    """Plot monthly sales values and counts on one axes."""
    months, values, counts = get_monthly_data(transactions, start_month, end_month, product_id)
    
    if not months:
        print("No data found for the given range.")
        return

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Month (YYYY-MM)')
    ax1.set_ylabel('Total Sales Value ($)', color=color)
    line1 = ax1.plot(months, values, color=color, marker='o', label='Sales Value')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Number of Sales', color=color)
    line2 = ax2.plot(months, counts, color=color, marker='s', label='Number of Sales')
    ax2.tick_params(axis='y', labelcolor=color)

    title = "Monthly Sales Performance"
    if product_name:
        title += f" - {product_name}"
    plt.title(title)
    
    # Combined legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.show()

def display_total_sales_bar_chart(transactions, groceries, start_date, end_date):
    """Display total sales per product in descending order."""
    product_sales = {g[0]: 0.0 for g in groceries[1:]}
    
    try:
        s_dt = datetime.strptime(start_date, "%d/%m/%Y")
        e_dt = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        print("Error: Invalid date format. Use DD/MM/YYYY.")
        return

    for t in transactions[1:]:
        try:
            t_dt = datetime.strptime(t[0], "%d/%m/%Y")
            if s_dt <= t_dt <= e_dt:
                product_sales[t[2]] += float(t[4])
        except (ValueError, KeyError):
            continue
            
    sorted_sales = sorted([(pid, val) for pid, val in product_sales.items() if val > 0], 
                          key=lambda x: x[1], reverse=True)
    
    if not sorted_sales:
        print("No sales data for this period.")
        return
        
    p_names = []
    p_values = []
    for pid, val in sorted_sales:
        name = next((g[1] for g in groceries[1:] if g[0] == pid), pid)
        p_names.append(name)
        p_values.append(val)
        
    plt.figure(figsize=(12, 6))
    plt.bar(p_names, p_values, color='skyblue')
    plt.xlabel('Grocery Product')
    plt.ylabel('Total Sales Value ($)')
    plt.title(f'Total Sales per Product ({start_date} to {end_date})')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def display_top_five_pie_chart(transactions, groceries, start_date, end_date):
    """Display top five products as percentage of total sales."""
    product_sales = {}
    total_sales = 0.0
    
    try:
        s_dt = datetime.strptime(start_date, "%d/%m/%Y")
        e_dt = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        print("Error: Invalid date format. Use DD/MM/YYYY.")
        return

    for t in transactions[1:]:
        try:
            t_dt = datetime.strptime(t[0], "%d/%m/%Y")
            if s_dt <= t_dt <= e_dt:
                pid = t[2]
                val = float(t[4])
                product_sales[pid] = product_sales.get(pid, 0.0) + val
                total_sales += val
        except (ValueError, KeyError):
            continue
            
    if total_sales == 0:
        print("No sales data for this period.")
        return
        
    sorted_sales = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
    
    top_five = sorted_sales[:5]
    others_val = sum(val for pid, val in sorted_sales[5:])
    
    labels = []
    sizes = []
    for pid, val in top_five:
        name = next((g[1] for g in groceries[1:] if g[0] == pid), pid)
        labels.append(name)
        sizes.append(val)
        
    if others_val > 0:
        labels.append("Others")
        sizes.append(others_val)
        
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(np.linspace(0, 1, len(labels))))
    plt.title(f'Top 5 Products Sales Share ({start_date} to {end_date})')
    plt.gca().text(0.5, -0.1, f"Total Sales Value: ${total_sales:.2f}", 
                   ha='center', va='center', transform=plt.gca().transAxes, fontsize=12, fontweight='bold')
    plt.show()
