import csv
from openpyxl import Workbook
import os
from pathlib import Path
h = Path.home()
os.makedirs(h / "Expenses", exist_ok=True )
FILENAME = h / "Expenses" / "expense.csv"
def create_csv():
    try:
        with open(FILENAME, "x", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["date", "amount", "category", "description"])
            writer.writeheader()
    except FileExistsError:
        pass
def add_expense(date, amount, category, description):
    with open(FILENAME, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "amount", "category", "description"])
        writer.writerow({"date": date, "amount": amount, "category": category, "description": description})
        print()
def view_expense():
    with open(FILENAME, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if reader:
            for row in reader:
                print("Row #" + str(reader.line_num), row["date"], row["amount"], row["category"], row["description"])
        elif not reader:
            print("No expense found")
def show_total_spending():
    with open(FILENAME, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        print(sum([float(i["amount"]) for i in reader]))
def spending_by_category(category):
    with open(FILENAME, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if category not in [i[category] for i in reader]:
            print("Category not found")
        else:
            for row in reader:
                if row["category"] == category:
                    print(row["date"], row["amount"], row["category"], row["description"])
            print(f"total spending by {row[category]}:{sum([i["amount"] for i in reader if i["category"] == category])}")
def show_highest_expense():
    with open(FILENAME, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        sorted_expenses = sorted([i["amount"] for i in reader])
        for row in reader:
            if sorted_expenses[0] == row["amount"]:
                print("your highest expense:", row["date"], row["amount"], row["category"], row["description"])
def export_to_excel(csvfile, excelfile):
    wb = Workbook()
    ws = wb.active
    with open(csvfile, "r", encoding="utf-8") as csv_obj:
        reader = csv.reader(csv_obj)
        for row in reader:
            ws.append(row)
        wb.save(excelfile)
def main():
    create_csv()
    print("_______Welcome_______")
    print("______Main Menu______")
    while True:
        navigation = str(input("to add expenses 'a'\n"
                           "to view expenses 'v'\n"
                           "to reports section 'r'\n"
                           "to get an exel copy 'e'\n"
                            "to quit 'q':"))
        if not navigation or not navigation.isalpha() or navigation not in ["a", "v", "r", "e"]:
            print("invalid input")
            continue
        elif navigation == "a":
            print("q to quit")
            while True:
                date = input("enter date(YYYY-MM-DD): ")
                amount = input("enter amount: ")
                category = input("enter category: ")
                description = input("enter description: ")
                if date == "q" or amount == "q" or category == "q" or description == "q":
                    break
                else:
                    add_expense(date=date, amount=amount, category=category, description=description)
        elif navigation == "v":
            view_expense()
        elif navigation == "r":
            print("______report section______")
            while True:
                reports_menu = str(input("show total spending: '1'\n"
                                        "Show spending by category: '2'\n"
                                        "Show highest expense: '3'\n"
                                        "back to main menu: '4'\n"))
                if reports_menu not in ["1", "2", "3", "4"]:
                    print("invalid input")
                    continue
                elif reports_menu == "1":
                    show_total_spending()
                elif reports_menu == "2":
                    while True:
                        s_category = input("enter a category(q to quit): ")
                        if s_category == "q":
                            break
                        else:
                            spending_by_category(category=s_category)
                elif reports_menu == "3":
                    show_highest_expense()
                elif reports_menu == "4":
                    break
        elif navigation == "e":
            export_to_excel(csvfile=FILENAME,excelfile=h / "Expenses" / "expense.xlsx")
            print("successfully exported to excel")

if __name__ == "__main__":

    main()

