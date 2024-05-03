import sqlite3
import csv
from datetime import datetime

class ExpenseTracker:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                amount REAL,
                                category TEXT,
                                date TEXT)''')
        self.conn.commit()

    def add_expense(self, amount, category):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''INSERT INTO expenses (amount, category, date)
                               VALUES (?, ?, ?)''', (amount, category, date))
        self.conn.commit()

    def total_expenses(self):
        self.cursor.execute('''SELECT SUM(amount) FROM expenses''')
        total = self.cursor.fetchone()[0]
        return total if total else 0

    def view_expenses(self, category=None, start_date=None, end_date=None):
        query = '''SELECT * FROM expenses'''
        params = ()

        if category:
            query += ''' WHERE category = ?'''
            params += (category,)

        if start_date and end_date:
            query += ''' AND date BETWEEN ? AND ?'''
            params += (start_date, end_date)
        elif start_date:
            query += ''' AND date >= ?'''
            params += (start_date,)
        elif end_date:
            query += ''' AND date <= ?'''
            params += (end_date,)

        self.cursor.execute(query, params)
        expenses = self.cursor.fetchall()
        return expenses

    def export_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Amount', 'Category', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for expense in self.view_expenses():
                writer.writerow({'ID': expense[0], 'Amount': expense[1], 'Category': expense[2], 'Date': expense[3]})

def main():
    tracker = ExpenseTracker('expenses.db')

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Total Expenses")
        print("3. View Expenses by Category")
        print("4. View Expenses by Date Range")
        print("5. Export Expenses to CSV")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter the amount: "))
            category = input("Enter the category: ")
            tracker.add_expense(amount, category)
            print("Expense added successfully!")

        elif choice == "2":
            print(f"Total expenses: ${tracker.total_expenses()}")

        elif choice == "3":
            category = input("Enter the category: ")
            expenses = tracker.view_expenses(category=category)
            if expenses:
                print("Expenses:")
                for expense in expenses:
                    print(f"ID: {expense[0]}, Amount: ${expense[1]}, Category: {expense[2]}, Date: {expense[3]}")
            else:
                print("No expenses found for this category.")

        elif choice == "4":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            expenses = tracker.view_expenses(start_date=start_date, end_date=end_date)
            if expenses:
                print("Expenses:")
                for expense in expenses:
                    print(f"ID: {expense[0]}, Amount: ${expense[1]}, Category: {expense[2]}, Date: {expense[3]}")
            else:
                print("No expenses found in this date range.")

        elif choice == "5":
            filename = input("Enter filename to export (e.g., expenses.csv): ")
            tracker.export_to_csv(filename)
            print("Expenses exported to CSV successfully!")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

    tracker.conn.close()

if __name__ == "__main__":
    main()
