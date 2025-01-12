"""The point of this program is to be a money spending tracker.
It allows you to keep track of your expenses by entering your expenses and you can then see your spending in 3 formats.
The first way is a pie chart that will show you what percentage of your spending was in each category.
The second way is a weekly spending bar graph. This allows you to see and compare how much you spent each week.
The third one is a non graphic format, where it just gives you the basic report of all spendings."""

import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Class for individual expenses
class Expense:
    def __init__(self, date, amount, category):
        self.date = datetime.strptime(date, "%Y-%m-%d")  # Convert string to date
        self.amount = float(amount)
        self.category = category

    def to_dict(self):
        return {"date": self.date.strftime("%Y-%m-%d"), "amount": self.amount, "category": self.category}


# Class for managing expenses
class ExpenseTracker:
    def __init__(self, csv_file="expenses.csv"):
        self.csv_file = csv_file
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)
        print(f"Added expense: {expense.category} - ${expense.amount} on {expense.date.strftime('%Y-%m-%d')}")

    def save_to_csv(self):
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "amount", "category"])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense.to_dict())
        print("Expenses saved to CSV file.")

    def load_from_csv(self):
        try:
            with open(self.csv_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.expenses.append(Expense(row["date"], row["amount"], row["category"]))
            print("Expenses loaded from CSV.")
        except FileNotFoundError:
            print("No existing file found. Starting fresh.")

    def get_expenses_dataframe(self):
        return pd.DataFrame([e.to_dict() for e in self.expenses])

    def generate_report(self):
        df = self.get_expenses_dataframe()
        if df.empty:
            print("No expenses to display.")
            return
        print("\nSpending Report:")
        print(df.groupby("category")["amount"].sum())
        print(f"Total Spending: ${df['amount'].sum():.2f}\n")


# Class for data visualization
class Visualizer:
    @staticmethod
    def plot_pie_chart(expenses_df):
        if expenses_df.empty:
            print("No data to show.")
            return
        category_data = expenses_df.groupby("category")["amount"].sum()
        category_data.plot.pie(autopct="%1.1f%%", startangle=90)
        plt.title("Spending by Category")
        plt.ylabel("")  # Remove default y-label
        plt.show()

    @staticmethod
    def plot_bar_chart(expenses_df):
        if expenses_df.empty:
            print("No data to visualize.")
            return
        expenses_df["week"] = expenses_df["date"].apply(lambda x: x.strftime("%U"))
        weekly_data = expenses_df.groupby("week")["amount"].sum()
        weekly_data.plot.bar(color="skyblue")
        plt.title("Weekly Spending")
        plt.xlabel("Week Number")
        plt.ylabel("Total Spending ($)")
        plt.show()


# Main Program
def main():
    tracker = ExpenseTracker()
    tracker.load_from_csv()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add a new expense")
        print("2. View spending report")
        print("3. View pie chart of spending by category")
        print("4. View bar chart of weekly spending")
        print("5. Save and Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            date = input("Enter the date (YYYY-MM-DD): ")
            amount = input("Enter the amount: ")
            category = input("Enter the category: ")
            expense = Expense(date, amount, category)
            tracker.add_expense(expense)
        elif choice == "2":
            tracker.generate_report()
        elif choice == "3":
            expenses_df = tracker.get_expenses_dataframe()
            Visualizer.plot_pie_chart(expenses_df)
        elif choice == "4":
            expenses_df = tracker.get_expenses_dataframe()
            expenses_df["date"] = pd.to_datetime(expenses_df["date"])  # Ensure proper date format
            Visualizer.plot_bar_chart(expenses_df)
        elif choice == "5":
            tracker.save_to_csv()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
