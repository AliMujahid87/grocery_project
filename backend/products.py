# products.py - product management stuff (add, update, delete, search)

import database


def get_all():
    return database.groceries_data


def search(term):
    if not term or term.strip() == '':
        return database.groceries_data
    return database.search_products(term.strip())


def add(name, price, stock):
    if not name or name.strip() == '':
        raise ValueError('Product name cant be empty')

    if price <= 0:
        raise ValueError('Price must be positive')
    if stock < 0:
        raise ValueError('Stock cant be negative')

    # check duplicates
    for p in database.groceries_data:
        if p['name'].lower() == name.strip().lower():
            raise ValueError(f'Product "{name}" already exists')

    new_prod = {
        'id': database.generate_new_id(),
        'name': name.strip(),
        'price': round(float(price), 2),
        'stock': int(stock)
    }
    database.groceries_data.append(new_prod)
    return new_prod


def update(pid, price=None, stock=None):
    prod = database.get_product_by_id(pid)
    if not prod:
        raise ValueError(f'Product "{pid}" not found')

    if price is not None:
        if price <= 0:
            raise ValueError('Price must be positive')
        prod['price'] = round(float(price), 2)

    if stock is not None:
        if stock < 0:
            raise ValueError('Stock cant be negative')
        prod['stock'] = int(stock)

    return prod
