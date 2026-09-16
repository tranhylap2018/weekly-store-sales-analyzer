import sys
import csv
import numpy as np

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")
elif len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")
else:
    filename = sys.argv[1]
    if not filename.endswith(".csv"):
        sys.exit("Not a CSV file")
try:
    with open(filename, "r") as file:
        filereader = csv.DictReader(file)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        sales = []
        for row in filereader:
            week = []
            for day in days:
                week.append(int(row[day]))
            sales.append(week)
        sales = np.array(sales)
        print(f"Sum of A: {sales[1].sum()}")
except FileNotFoundError:
    sys.exit("File does not exist")
