import csv

def load_csv(filename):
    """Load data from a CSV file into a list of lists."""
    data = []
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return data

def save_csv(filename, data):
    """Save a list of lists to a CSV file."""
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
