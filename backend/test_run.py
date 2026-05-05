import os, sys
# ensure current folder is on PYTHONPATH
sys.path.append(os.path.abspath('.'))

# use a non‑interactive backend so plt.show() won’t hang
import matplotlib
matplotlib.use('Agg')

import database, auth, transactions, analytics

base_dir = os.path.dirname(os.path.abspath(__file__))
groceries_csv = os.path.join(base_dir, 'data', 'groceries.csv')
transactions_csv = os.path.join(base_dir, 'data', 'transactions.csv')
users_csv = os.path.join(base_dir, 'data', 'users.csv')

# load data
database.initialize(groceries_csv, transactions_csv, users_csv)
print('Loaded', len(database.groceries_data), 'products')
print('Loaded', len(database.transactions_data), 'transactions')

# test login
user = auth.authenticate('manager1', 'manager123')
print('Login result:', user)

# add a sale – 2 of G01
sale = transactions.add_transaction('G01', 2)
print('Added sale:', sale)

# generate a chart (saved to file, no pop‑up)
analytics.monthly_sales_chart('2023-08', '2024-01')

# flush changes back to CSVs
database.flush_all()
print('Data flushed, script finished')
