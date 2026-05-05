# analytics.py - generates charts using matplotlib and numpy
# had some trouble getting the dual axis to work properly at first

import os
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

import database

CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')

# color scheme
MAIN_COLOR = '#2C3539'
ACCENT_COLOR = '#AB274F'
ACCENT2 = '#D4826A'  # secondary accent for second line
BG_COLOR = '#F5F0EB'
GRID_COLOR = '#C8C2BC'


def _make_charts_dir():
    os.makedirs(CHARTS_DIR, exist_ok=True)


def _filter_by_period(start_date, end_date):
    """helper - grabs transactions within a date range"""
    filtered = []
    try:
        s = datetime.strptime(start_date, '%Y-%m-%d')
        e = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
    except (ValueError, TypeError):
        return database.transactions_data

    for txn in database.transactions_data:
        try:
            d = datetime.strptime(txn['date'], '%Y-%m-%d %H:%M:%S')
            if s <= d <= e:
                filtered.append(txn)
        except (ValueError, TypeError):
            continue
    return filtered


def _style_chart(fig, ax):
    """applies my color scheme to a chart"""
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor('#FAFAF7')
    ax.tick_params(colors=MAIN_COLOR, labelsize=9)
    ax.xaxis.label.set_color(MAIN_COLOR)
    ax.yaxis.label.set_color(MAIN_COLOR)
    ax.title.set_color(MAIN_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(True, color=GRID_COLOR, alpha=0.4, linestyle='-')


def monthly_sales_chart(start_month, end_month):
    """line chart - monthly revenue + number of sales"""
    _make_charts_dir()

    monthly_rev = defaultdict(float)
    monthly_count = defaultdict(int)

    for txn in database.transactions_data:
        try:
            dt = datetime.strptime(txn['date'], '%Y-%m-%d %H:%M:%S')
            key = dt.strftime('%Y-%m')
            if key < start_month or key > end_month:
                continue
            monthly_rev[key] += float(txn['payment'])
            monthly_count[key] += 1
        except (ValueError, TypeError):
            continue

    if not monthly_rev:
        print("No data found for that period.")
        return

    months = sorted(monthly_rev.keys())
    labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in months]
    revs = [round(monthly_rev[m], 2) for m in months]
    counts = [monthly_count[m] for m in months]

    fig, ax1 = plt.subplots(figsize=(11, 5))
    _style_chart(fig, ax1)

    ax1.plot(labels, revs, color=ACCENT_COLOR, marker='o', linewidth=2,
             markersize=6, label='Sales Value ($)')
    ax1.set_xlabel('Month', fontsize=11)
    ax1.set_ylabel('Sales Value ($)', color=ACCENT_COLOR, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=ACCENT_COLOR)

    ax2 = ax1.twinx()
    ax2.plot(labels, counts, color=ACCENT2, marker='s', linewidth=2,
             markersize=6, linestyle='--', label='Number of Sales')
    ax2.set_ylabel('Number of Sales', color=ACCENT2, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=ACCENT2)

    fig.suptitle(f'Monthly Sales ({start_month} to {end_month})',
                 fontsize=14, fontweight='bold', color=MAIN_COLOR)

    # combined legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=9)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    path = os.path.join(CHARTS_DIR, 'monthly_sales.png')
    fig.savefig(path, dpi=120, bbox_inches='tight')
    plt.show()
    plt.close(fig)


def product_monthly_chart(pid, start_month, end_month):
    """line chart for a specific product's monthly performance"""
    _make_charts_dir()

    prod = database.get_product_by_id(pid)
    if not prod:
        print(f"Product '{pid}' not found.")
        return

    monthly_rev = defaultdict(float)
    monthly_count = defaultdict(int)

    for txn in database.transactions_data:
        if txn['product_id'] != pid:
            continue
        try:
            dt = datetime.strptime(txn['date'], '%Y-%m-%d %H:%M:%S')
            key = dt.strftime('%Y-%m')
            if key < start_month or key > end_month:
                continue
            monthly_rev[key] += float(txn['payment'])
            monthly_count[key] += 1
        except (ValueError, TypeError):
            continue

    if not monthly_rev:
        print(f"No data for '{prod['name']}' in that period.")
        return

    months = sorted(monthly_rev.keys())
    labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in months]
    revs = [round(monthly_rev[m], 2) for m in months]
    counts = [monthly_count[m] for m in months]

    fig, ax1 = plt.subplots(figsize=(11, 5))
    _style_chart(fig, ax1)

    ax1.plot(labels, revs, color=ACCENT_COLOR, marker='o', linewidth=2,
             markersize=6, label='Sales Value ($)')
    ax1.set_xlabel('Month', fontsize=11)
    ax1.set_ylabel('Sales Value ($)', color=ACCENT_COLOR, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=ACCENT_COLOR)

    ax2 = ax1.twinx()
    ax2.plot(labels, counts, color=ACCENT2, marker='s', linewidth=2,
             markersize=6, linestyle='--', label='Number of Sales')
    ax2.set_ylabel('Number of Sales', color=ACCENT2, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=ACCENT2)

    fig.suptitle(f'{prod["name"]} - Monthly Sales ({start_month} to {end_month})',
                 fontsize=14, fontweight='bold', color=MAIN_COLOR)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=9)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    path = os.path.join(CHARTS_DIR, 'product_monthly.png')
    fig.savefig(path, dpi=120, bbox_inches='tight')
    plt.show()
    plt.close(fig)


def product_bar_chart(start_date, end_date):
    """bar chart - all products sorted by revenue descending"""
    _make_charts_dir()

    txns = _filter_by_period(start_date, end_date)
    rev_by_product = defaultdict(float)
    for txn in txns:
        rev_by_product[txn['product_id']] += float(txn['payment'])

    if not rev_by_product:
        print("No data for that period.")
        return

    # sort descending
    sorted_items = sorted(rev_by_product.items(), key=lambda x: x[1], reverse=True)

    names = []
    values = []
    for pid, rev in sorted_items:
        p = database.get_product_by_id(pid)
        names.append(p['name'] if p else pid)
        values.append(round(rev, 2))

    fig, ax = plt.subplots(figsize=(12, 6))
    _style_chart(fig, ax)

    # gradient-ish colors from accent
    n = len(names)
    bar_colors = [ACCENT_COLOR] * n
    # make bars slightly lighter as they go down
    for i in range(n):
        alpha = 1.0 - (i * 0.04)
        if alpha < 0.4:
            alpha = 0.4
        bar_colors[i] = ACCENT_COLOR  # keeping it simple, same color

    bars = ax.bar(range(n), values, color=ACCENT_COLOR, width=0.65, alpha=0.85)

    # value labels on top
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f'${val:.2f}', ha='center', va='bottom', fontsize=8, color=MAIN_COLOR)

    ax.set_xticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax.set_xlabel('Product', fontsize=11)
    ax.set_ylabel('Total Sales Value ($)', fontsize=11)
    ax.set_title(f'Product Sales - Descending ({start_date} to {end_date})',
                 fontsize=14, fontweight='bold', color=MAIN_COLOR, pad=15)

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, 'product_bar.png')
    fig.savefig(path, dpi=120, bbox_inches='tight')
    plt.show()
    plt.close(fig)


def top5_pie_chart(start_date, end_date):
    """pie chart - top 5 products + others"""
    _make_charts_dir()

    txns = _filter_by_period(start_date, end_date)
    rev_by_product = defaultdict(float)
    for txn in txns:
        rev_by_product[txn['product_id']] += float(txn['payment'])

    if not rev_by_product:
        print("No data for that period.")
        return

    sorted_items = sorted(rev_by_product.items(), key=lambda x: x[1], reverse=True)

    labels = []
    sizes = []
    others_total = 0

    for i, (pid, rev) in enumerate(sorted_items):
        if i < 5:
            p = database.get_product_by_id(pid)
            labels.append(p['name'] if p else pid)
            sizes.append(round(rev, 2))
        else:
            others_total += rev

    if others_total > 0:
        labels.append('Others')
        sizes.append(round(others_total, 2))

    # colors for the pie slices
    pie_colors = [ACCENT_COLOR, ACCENT2, '#7B886B', '#C4A35A', '#6B7D8B', GRID_COLOR]
    pie_colors = pie_colors[:len(labels)]

    explode = [0.03] * len(labels)

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(BG_COLOR)

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=140,
        colors=pie_colors, explode=explode, pctdistance=0.75,
        wedgeprops=dict(linewidth=1.5, edgecolor=BG_COLOR)
    )

    for t in texts:
        t.set_color(MAIN_COLOR)
        t.set_fontsize(10)
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight('bold')

    ax.set_title(f'Top 5 Products by Sales Value\n({start_date} to {end_date})',
                 fontsize=14, fontweight='bold', color=MAIN_COLOR, pad=15)

    # caption with total
    total = sum(sizes)
    fig.text(0.5, 0.02, f'Total Sales Value: ${total:.2f}',
             ha='center', fontsize=10, color=MAIN_COLOR, fontstyle='italic')

    # legend
    leg_labels = [f'{l}: ${s:.2f}' for l, s in zip(labels, sizes)]
    ax.legend(leg_labels, loc='lower right', fontsize=8)

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, 'top5_pie.png')
    fig.savefig(path, dpi=120, bbox_inches='tight')
    plt.show()
    plt.close(fig)
