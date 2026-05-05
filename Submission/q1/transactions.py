# transactions.py - handles sales transactions, searching, filtering

from datetime import datetime
import database


def add_transaction(pid, qty):
    prod = database.get_product_by_id(pid)
    if not prod:
        raise ValueError(f'Product "{pid}" not found')

    qty = int(qty)
    if qty <= 0:
        raise ValueError('Quantity must be greater than 0')

    if prod['stock'] < qty:
        raise ValueError(
            f'Not enough stock for "{prod["name"]}". '
            f'Available: {prod["stock"]}, Requested: {qty}'
        )

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payment = round(qty * prod['price'], 2)

    txn = {
        'date': now,
        'product_id': pid,
        'qty': qty,
        'payment': payment
    }

    prod['stock'] -= qty
    database.transactions_data.append(txn)

    # return extra info for display
    return {
        **txn,
        'product_name': prod['name'],
        'unit_price': prod['price'],
        'remaining_stock': prod['stock']
    }


def get_all():
    """returns all transactions with product names attached"""
    result = []
    for txn in database.transactions_data:
        prod = database.get_product_by_id(txn['product_id'])
        name = prod['name'] if prod else 'Unknown'
        result.append({**txn, 'product_name': name})
    return result


def filter_by_date(start_str, end_str):
    try:
        start = datetime.strptime(start_str, '%Y-%m-%d')
        end = datetime.strptime(end_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        raise ValueError('Bad date format. Use YYYY-MM-DD')

    if start > end:
        raise ValueError('Start date cant be after end date')

    # include the whole end day
    end = end.replace(hour=23, minute=59, second=59)

    filtered = []
    for txn in database.transactions_data:
        try:
            txn_date = datetime.strptime(txn['date'], '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            continue

        if start <= txn_date <= end:
            prod = database.get_product_by_id(txn['product_id'])
            name = prod['name'] if prod else 'Unknown'
            filtered.append({**txn, 'product_name': name})

    return filtered


def search_by_name(term):
    """search transactions by product name - partial match, case insensitive"""
    results = []
    all_txns = get_all()
    for txn in all_txns:
        if term.lower() in txn['product_name'].lower():
            results.append(txn)
    return results


def search_by_name_and_date(term, start_str, end_str):
    """combined search - filter by name AND date range"""
    date_results = filter_by_date(start_str, end_str)
    filtered = []
    for txn in date_results:
        if term.lower() in txn['product_name'].lower():
            filtered.append(txn)
    return filtered
