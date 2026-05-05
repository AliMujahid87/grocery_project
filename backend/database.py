# database.py - handles all the csv reading/writing and stores data in memory

import csv
import os

# global lists that hold everything
groceries_data = []
transactions_data = []
users_data = []

# paths to the csv files
groceries_path = ''
transactions_path = ''
users_path = ''


def load_csv(filepath):
    """reads a csv file and returns list of dicts"""
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))
    return data


def save_csv(filepath, data, fieldnames):
    """writes list of dicts back to csv"""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def initialize(g_path, t_path, u_path):
    global groceries_data, transactions_data, users_data
    global groceries_path, transactions_path, users_path

    groceries_path = g_path
    transactions_path = t_path
    users_path = u_path

    groceries_data = load_csv(groceries_path)
    transactions_data = load_csv(transactions_path)
    users_data = load_csv(users_path)

    # convert the numeric fields from strings
    for row in groceries_data:
        try:
            row['price'] = float(row['price'])
            row['stock'] = int(row['stock'])
        except (ValueError, KeyError):
            pass

    for row in transactions_data:
        try:
            row['qty'] = int(row['qty'])
            row['payment'] = float(row['payment'])
        except (ValueError, KeyError):
            pass


def flush_all():
    """saves everything back to csv files - called on logout"""
    if groceries_path and groceries_data:
        save_csv(groceries_path, groceries_data, ['id', 'name', 'price', 'stock'])

    if transactions_path:
        save_csv(transactions_path, transactions_data, ['date', 'product_id', 'qty', 'payment'])

    # dont overwrite users file unless we need to
    if users_path and users_data:
        save_csv(users_path, users_data, ['username', 'password', 'role'])


def search_products(term):
    """partial case-insensitive search on product names"""
    results = []
    for p in groceries_data:
        if term.lower() in p['name'].lower():
            results.append(p)
    return results


def get_product_by_id(pid):
    for p in groceries_data:
        if p['id'] == pid:
            return p
    return None


def generate_new_id():
    if not groceries_data:
        return 'G01'

    max_num = 0
    for p in groceries_data:
        try:
            num = int(p['id'][1:])
            if num > max_num:
                max_num = num
        except (ValueError, IndexError):
            continue
    return f'G{max_num + 1:02d}'
