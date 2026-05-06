# ICT582 Assignment Documentation

## Assignment Check List
- [x] Question 1 implemented and tested.
- [x] Question 2 implemented and tested (Modular design).
- [x] Question 3 implemented and tested (Graphical analysis).
- [x] Adhered to naming conventions.
- [x] All required files included in separate folders.
- [x] Test evidence provided.

## Table of Contents
1. [Question 1: Simple Management System](#question-1)
2. [Question 2: Search and Manipulation](#question-2)
3. [Question 3: Graphical Performance Display](#question-3)
4. [File List](#file-list)

---

<a name="question-1"></a>
## Question 1: A simple management system for a grocery store

### Discussion of Solution
The solution for Question 1 implements a basic CLI-based management system. Data is stored in CSV format and loaded into memory as a list of dictionaries for efficient access. Authentication is handled via `users.csv` with role-based access (Cashier vs Manager).
- **Technical Choices**: Used the built-in `csv` module for reliability and `datetime` for automatic timestamping.
- **Strengths**: Robust validation for product IDs and stock levels.
- **Weaknesses**: The in-memory data structure is efficient for small datasets but would require a database for larger ones.

### Self-diagnosis and Evaluation
- **Feature: Load/Save CSV**: Fully working.
- **Feature: Authentication**: Fully working.
- **Feature: Enter Sales**: Fully working (updates stock and records transaction).
- **Feature: Add Grocery (Manager)**: Fully working.
- **Feature: Logout/Save**: Fully working.

### Test Evidence
**Test: Authentication and Sales Entry**
```
Enter username: john
Enter password: john
Login successful! Welcome john (cashier).

--- Grocery ID - Name Mapping ---
ID: 1 - Name: Apple
ID: 4 - Name: Milk
...
Select an option: 1
Enter Grocery ID: 4
Enter quantity for Milk: 2
Enter payment received: 4.2
Transaction added successfully.
```
**Conclusion**: Test successful. Stock was reduced and transaction recorded.

---

<a name="question-2"></a>
## Question 2: Search and manipulation of sales and grocery records

### Discussion of Solution
Question 2 introduces a modular design, separating data handling (`data_handler.py`) and business logic (`operations.py`) from the user interface (`main.py`). This adheres to the DRY (Don't Repeat Yourself) principle and improves maintainability.
- **Technical Choices**: Implemented partial string matching and case-insensitive search using Python's string methods.
- **Novelty**: Used a modular approach even for simple CLI tools to demonstrate architectural skills.

### Self-diagnosis and Evaluation
- **Feature: Modular Design**: Fully working (3 modules).
- **Feature: Search by Date**: Fully working.
- **Feature: Search by Name (Partial/Case-insensitive)**: Fully working.
- **Feature: Search by Name & Date Range**: Fully working.
- **Feature: Update Grocery (Manager)**: Fully working.

### Test Evidence
**Test: Search by Product Name "milk"**
```
Enter product name (partial): milk

Transactions for products matching 'milk':
Date         | Time         | Product              | Qty   | Payment 
04/05/2023   | 4:08:22 PM   | Milk                 | 5     | 10.5    
...
```
**Conclusion**: Test successful. All "Milk" transactions were retrieved correctly regardless of case or partial matching.

---

<a name="question-3"></a>
## Question 3: Display sales performance graphically

### Discussion of Solution
Question 3 leverages `numpy` and `matplotlib` for data visualization. The `analytics.py` module processes raw transaction data to generate monthly trends and distribution charts.
- **Technical Choices**: Used dual-axis plots for line graphs to show both volume and value simultaneously.
- **Strengths**: Interactive charts provide immediate insights into store performance.

### Self-diagnosis and Evaluation
- **Feature: Monthly Line Graphs**: Fully working.
- **Feature: Product Line Graphs**: Fully working.
- **Feature: Total Sales Bar Chart**: Fully working (Sorted descending).
- **Feature: Top 5 Pie Chart**: Fully working (with "Others" category).

### Test Evidence
**Test: Monthly Performance (2023-04 to 2023-12)**
- *Logic verified*: Data is aggregated by `YYYY-MM` key after parsing `DD/MM/YYYY`.
- *Plotting*: `twinx()` ensures Value and Count scales are distinct.
**Conclusion**: Code executes without errors and produces required visualizations.

---

<a name="file-list"></a>
## File List
### Question 1
- `q1/main.py`
- `q1/transactions.csv`
- `q1/groceries.csv`
- `q1/users.csv`

### Question 2
- `q2/main.py`
- `q2/data_handler.py`
- `q2/operations.py`
- `q2/transactions.csv`
- `q2/groceries.csv`
- `q2/users.csv`

### Question 3
- `q3/main.py`
- `q3/data_handler.py`
- `q3/operations.py`
- `q3/analytics.py`
- `q3/transactions.csv`
- `q3/groceries.csv`
- `q3/users.csv`
