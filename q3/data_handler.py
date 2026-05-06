import csv

def load_csv(filename):
    """Load data from a CSV file into a list of dictionaries."""
    data = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return data

def save_csv(filename, data, fieldnames):
    """Save a list of dictionaries to a CSV file."""
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
