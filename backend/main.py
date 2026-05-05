"""
main.py — Flask Application Entry Point & API Routes

This is the main entry point for the Grocery Store Management System backend.
It handles:
- sys.argv parsing for CSV file paths
- Data initialization (loading CSVs into memory)
- All REST API route definitions
- CORS configuration for frontend communication

Usage:
    python main.py [groceries.csv path] [transactions.csv path]
    
    Defaults to data/groceries.csv and data/transactions.csv if no args given.
"""

import sys
import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

import database
import auth
import products as products_module
import transactions as transactions_module
import analytics


# =============================================================================
# APP INITIALIZATION
# =============================================================================

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend


def initialize_data():
    """Parse sys.argv for CSV paths and load all data into memory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    transactions_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base_dir, 'data', 'transactions.csv')
    groceries_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(base_dir, 'data', 'groceries.csv')
    users_path = os.path.join(base_dir, 'data', 'users.csv')

    print(f'[INIT] Loading transactions from: {transactions_path}')
    print(f'[INIT] Loading groceries from: {groceries_path}')
    print(f'[INIT] Loading users from: {users_path}')

    database.initialize(groceries_path, transactions_path, users_path)

    print(f'[INIT] Loaded {len(database.groceries_data)} products')
    print(f'[INIT] Loaded {len(database.transactions_data)} transactions')
    print(f'[INIT] Loaded {len(database.users_data)} users')
    print('[INIT] System ready!')


# =============================================================================
# ROOT ROUTE — API Info
# =============================================================================

@app.route('/', methods=['GET'])
def api_root():
    """Root endpoint — shows API status and available endpoints."""
    return jsonify({
        'status': 'running',
        'application': 'Grocery Store Management System API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'POST /api/login': 'Authenticate user (body: username, password)',
                'POST /api/logout': 'Logout & save data (requires token)',
                'GET /api/user/role': 'Get current user role (requires token)',
            },
            'products': {
                'GET /api/products': 'List all products',
                'GET /api/products/search?q=': 'Search products (partial, case-insensitive)',
                'POST /api/products': 'Add new product (Manager only)',
                'PUT /api/products/<id>': 'Update product (Manager only)',
                'DELETE /api/products/<id>': 'Delete product (Manager only)',
            },
            'transactions': {
                'GET /api/transactions': 'List all transactions',
                'POST /api/transactions': 'Add new transaction (body: product_id, qty)',
                'GET /api/transactions/filter?start=&end=': 'Filter by date range',
                'GET /api/transactions/summary?date=': 'Daily summary',
            },
            'analytics': {
                'GET /api/analytics/monthly': 'Monthly sales line chart (Manager only)',
                'GET /api/analytics/products': 'Product sales bar chart (Manager only)',
                'GET /api/analytics/top5': 'Top-5 pie chart (Manager only)',
            },
            'overview': {
                'GET /api/overview': 'Dashboard stats overview',
            }
        }
    }), 200


# =============================================================================
# AUTH ROUTES
# =============================================================================

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user and return a session token."""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required.'}), 400

    user_info = auth.authenticate(data['username'], data['password'])

    if not user_info:
        return jsonify({'error': 'Invalid username or password.'}), 401

    token = auth.create_session(user_info)

    return jsonify({
        'message': f'Welcome, {user_info["username"]}!',
        'token': token,
        'username': user_info['username'],
        'role': user_info['role']
    }), 200


@app.route('/api/logout', methods=['POST'])
@auth.login_required
def logout(current_user):
    """Flush all data to CSV and destroy session."""
    token = request.headers.get('Authorization', '')[7:]

    # Flush in-memory data to CSV files
    database.flush_all()
    print(f'[FLUSH] Data saved to CSV files by user: {current_user["username"]}')

    # Destroy session
    auth.destroy_session(token)

    return jsonify({
        'message': 'Logged out successfully. All data saved.'
    }), 200


@app.route('/api/user/role', methods=['GET'])
@auth.login_required
def get_user_role(current_user):
    """Returns the current user's role and username."""
    return jsonify({
        'username': current_user['username'],
        'role': current_user['role']
    }), 200


# =============================================================================
# PRODUCT ROUTES
# =============================================================================

@app.route('/api/products', methods=['GET'])
@auth.login_required
def get_products(current_user):
    """List all products."""
    all_products = products_module.get_all_products()
    return jsonify({
        'products': all_products,
        'count': len(all_products)
    }), 200


@app.route('/api/products/search', methods=['GET'])
@auth.login_required
def search_products(current_user):
    """Search products with partial, case-insensitive matching."""
    query = request.args.get('q', '')
    results = products_module.search_products(query)
    return jsonify({
        'products': results,
        'count': len(results),
        'query': query
    }), 200


@app.route('/api/products', methods=['POST'])
@auth.login_required
@auth.role_required('manager')
def add_product(current_user):
    """Add a new product (Manager only)."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required.'}), 400

    required = ['name', 'price', 'stock']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Field "{field}" is required.'}), 400

    try:
        new_product = products_module.add_product(
            data['name'], float(data['price']), int(data['stock'])
        )
        return jsonify({
            'message': f'Product "{new_product["name"]}" added successfully.',
            'product': new_product
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/products/<product_id>', methods=['PUT'])
@auth.login_required
@auth.role_required('manager')
def update_product(product_id, current_user):
    """Update a product's price, stock, or name (Manager only)."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required.'}), 400

    try:
        updated = products_module.update_product(
            product_id,
            price=float(data['price']) if 'price' in data else None,
            stock=int(data['stock']) if 'stock' in data else None,
            name=data.get('name')
        )
        return jsonify({
            'message': f'Product "{updated["name"]}" updated successfully.',
            'product': updated
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/products/<product_id>', methods=['DELETE'])
@auth.login_required
@auth.role_required('manager')
def delete_product(product_id, current_user):
    """Delete a product (Manager only)."""
    try:
        deleted = products_module.delete_product(product_id)
        return jsonify({
            'message': f'Product "{deleted["name"]}" deleted successfully.',
            'product': deleted
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# =============================================================================
# TRANSACTION ROUTES
# =============================================================================

@app.route('/api/transactions', methods=['GET'])
@auth.login_required
def get_transactions(current_user):
    """List all transactions."""
    all_txns = transactions_module.get_all_transactions()
    return jsonify({
        'transactions': all_txns,
        'count': len(all_txns)
    }), 200


@app.route('/api/transactions', methods=['POST'])
@auth.login_required
def add_transaction(current_user):
    """Add a new transaction (sale)."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body is required.'}), 400

    if 'product_id' not in data or 'qty' not in data:
        return jsonify({'error': 'Fields "product_id" and "qty" are required.'}), 400

    try:
        txn = transactions_module.add_transaction(
            data['product_id'], int(data['qty'])
        )
        return jsonify({
            'message': 'Transaction recorded successfully.',
            'transaction': txn
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/transactions/filter', methods=['GET'])
@auth.login_required
def filter_transactions(current_user):
    """Filter transactions by date range."""
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({'error': 'Both "start" and "end" date parameters are required.'}), 400

    try:
        filtered = transactions_module.filter_by_date(start, end)
        total_revenue = sum(t['payment'] for t in filtered)
        total_items = sum(t['qty'] for t in filtered)
        return jsonify({
            'transactions': filtered,
            'count': len(filtered),
            'total_revenue': round(total_revenue, 2),
            'total_items': total_items,
            'date_range': {'start': start, 'end': end}
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/transactions/summary', methods=['GET'])
@auth.login_required
def daily_summary(current_user):
    """Get a daily transaction summary."""
    date = request.args.get('date')
    if not date:
        return jsonify({'error': 'The "date" parameter is required.'}), 400

    try:
        summary = transactions_module.get_daily_summary(date)
        return jsonify(summary), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# =============================================================================
# ANALYTICS ROUTES (Manager Only)
# =============================================================================

@app.route('/api/analytics/monthly', methods=['GET'])
@auth.login_required
@auth.role_required('manager')
def monthly_chart(current_user):
    """Generate and return the monthly sales line chart."""
    path = analytics.generate_monthly_sales_chart()
    if not path:
        return jsonify({'error': 'No transaction data available for chart.'}), 404
    return send_file(path, mimetype='image/png')


@app.route('/api/analytics/products', methods=['GET'])
@auth.login_required
@auth.role_required('manager')
def products_chart(current_user):
    """Generate and return the product sales bar chart."""
    path = analytics.generate_product_bar_chart()
    if not path:
        return jsonify({'error': 'No transaction data available for chart.'}), 404
    return send_file(path, mimetype='image/png')


@app.route('/api/analytics/top5', methods=['GET'])
@auth.login_required
@auth.role_required('manager')
def top5_chart(current_user):
    """Generate and return the top-5 pie chart."""
    path = analytics.generate_top5_pie_chart()
    if not path:
        return jsonify({'error': 'No transaction data available for chart.'}), 404
    return send_file(path, mimetype='image/png')


# =============================================================================
# OVERVIEW / STATS ROUTE
# =============================================================================

@app.route('/api/overview', methods=['GET'])
@auth.login_required
def get_overview(current_user):
    """Returns dashboard overview statistics."""
    total_products = len(database.groceries_data)
    total_transactions = len(database.transactions_data)
    total_revenue = round(sum(float(t['payment']) for t in database.transactions_data), 2)
    low_stock = [p for p in database.groceries_data if p['stock'] <= 10]

    recent = transactions_module.get_all_transactions()[-5:]
    recent.reverse()

    return jsonify({
        'total_products': total_products,
        'total_transactions': total_transactions,
        'total_revenue': total_revenue,
        'low_stock_count': len(low_stock),
        'low_stock_items': low_stock,
        'recent_transactions': recent
    }), 200


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    initialize_data()
    print('\n[SERVER] Starting Flask server on http://localhost:5000')
    print('[SERVER] Press Ctrl+C to stop\n')
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
