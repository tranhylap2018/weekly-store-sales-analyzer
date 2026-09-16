import csv
import numpy as np
from pathlib import Path


DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
PRODUCTS = ["A", "B", "C", "D"]


def load_week(filename):
    sales = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            week = []

            for day in DAYS:
                week.append(int(row[day]))

            sales.append(week)

    return np.array(sales)


def main():
    # analyzer.py is inside script/
    project_folder = Path(__file__).parent.parent

    data_folder = project_folder / "data"

    # Load all 4 weeks
    week1 = load_week(data_folder / "week1.csv")
    week2 = load_week(data_folder / "week2.csv")
    week3 = load_week(data_folder / "week3.csv")
    week4 = load_week(data_folder / "week4.csv")


    # (4 weeks, 4 products, 7 days)
    all_sales = np.stack([
        week1,
        week2,
        week3,
        week4
    ])


# Basic information
    dataset_shape = all_sales.shape
    dataset_dimensions = all_sales.ndim
    dataset_size = all_sales.size

# Weekly total

    # axis 1 = products
    # axis 2 = days

    weekly_totals = all_sales.sum(axis=(1, 2))

    best_week_index = np.argmax(weekly_totals)
    best_week = best_week_index + 1

# Product totals

    # Sum weeks + days
    # Keep product.
    product_totals = all_sales.sum(axis=(0, 2))

    best_product_index = np.argmax(product_totals)
    best_product = PRODUCTS[best_product_index]

# Product averages

    product_averages = all_sales.mean(axis=(0, 2))

# Sale by day

    # Sum weeks + products
    # Keep days.
    daily_totals = all_sales.sum(axis=(0, 1))

    best_day_index = np.argmax(daily_totals)
    best_day = DAYS[best_day_index]

# Weekend

    # Mon-Fri = indexes 0-4
    weekdays = all_sales[:, :, :5]

    # Sat-Sun = indexes 5-6
    weekends = all_sales[:, :, 5:]

    weekday_total = weekdays.sum()
    weekend_total = weekends.sum()

    if weekday_total > weekend_total:
        higher_period = "Weekdays"
    elif weekend_total > weekday_total:
        higher_period = "Weekend"
    else:
        higher_period = "Equal"

# High sales

    high_sales = all_sales[all_sales >= 30]

# Weekly trends


    product_weekly_totals = all_sales.sum(axis=2)

# Save report to output.txt

    output_file = project_folder / "output.txt"

    with open(output_file, "w") as file:

        file.write("======== MONTHLY SALES REPORT ========\n\n")

        file.write("--- DATASET INFORMATION ---\n")
        file.write(f"Shape: {dataset_shape}\n")
        file.write(f"Dimensions: {dataset_dimensions}\n")
        file.write(f"Number of values: {dataset_size}\n\n")

        # Weekly totals
        file.write("--- WEEKLY TOTALS ---\n")

        for i in range(4):
            file.write(
                f"Week {i + 1}: {weekly_totals[i]} units\n"
            )

        file.write(
            f"\nBest week: Week {best_week} "
            f"({weekly_totals[best_week_index]} units)\n\n"
        )

        # Product totals
        file.write("--- PRODUCT TOTALS ---\n")

        for i in range(len(PRODUCTS)):
            file.write(
                f"Product {PRODUCTS[i]}: "
                f"{product_totals[i]} units\n"
            )

        file.write(
            f"\nBest-selling product: Product {best_product} "
            f"({product_totals[best_product_index]} units)\n\n"
        )

        # Product averages
        file.write("--- PRODUCT AVERAGES ---\n")

        for i in range(len(PRODUCTS)):
            file.write(
                f"Product {PRODUCTS[i]}: "
                f"{product_averages[i]:.2f} units/day\n"
            )

        file.write("\n")

        # Daily totals
        file.write("--- SALES BY DAY OF WEEK ---\n")

        for i in range(len(DAYS)):
            file.write(
                f"{DAYS[i]}: {daily_totals[i]} units\n"
            )

        file.write(
            f"\nBusiest day: {best_day} "
            f"({daily_totals[best_day_index]} units)\n\n"
        )

        # Weekday vs weekend
        file.write("--- WEEKDAY VS WEEKEND ---\n")
        file.write(f"Weekday total: {weekday_total}\n")
        file.write(f"Weekend total: {weekend_total}\n")
        file.write(f"Higher sales period: {higher_period}\n\n")

        # High sales
        file.write("--- HIGH SALES VALUES ---\n")
        file.write("Individual sales >= 30:\n")
        file.write(f"{high_sales}\n\n")

        # Product trends
        file.write("--- PRODUCT WEEKLY TRENDS ---\n")

        for product_index in range(len(PRODUCTS)):

            file.write(
                f"\nProduct {PRODUCTS[product_index]}:\n"
            )

            for week_index in range(4):

                file.write(
                    f"Week {week_index + 1}: "
                    f"{product_weekly_totals[week_index, product_index]} "
                    f"units\n"
                )

    print("Analysis complete!")
    print(f"Report saved to: {output_file}")


if __name__ == "__main__":
    main()