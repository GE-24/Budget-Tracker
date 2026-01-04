# 50/30/20 Personal Budget Tracker - Pro Version with Running Balances
# Author: Gabriel Enrique

import matplotlib.pyplot as plt
import csv
from datetime import datetime

class BudgetCategory:
    def __init__(self, name, allocation):
        self.name = name
        self.allocation = allocation
        self.expenses = []

    def add_expense(self, amount, description=""):
        self.expenses.append((description, amount))

    def total_spent(self):
        return sum(amount for _, amount in self.expenses)

    def remaining_budget(self):
        return self.allocation - self.total_spent()

    def is_over_budget(self):
        return self.total_spent() > self.allocation

    def running_balances(self):
        """Returns a list of (description, amount, remaining_budget) for each expense"""
        balances = []
        total = 0
        for desc, amt in self.expenses:
            total += amt
            balances.append((desc if desc else "No description", amt, self.allocation - total))
        return balances

class BudgetTracker:
    def __init__(self, salary):
        self.salary = salary
        self.categories = {
            "Needs": BudgetCategory("Needs", 0.5 * salary),
            "Wants": BudgetCategory("Wants", 0.3 * salary),
            "Savings": BudgetCategory("Savings", 0.2 * salary)
        }

    def add_expense(self, category_name, amount, description=""):
        cat = self.categories[category_name]
        cat.add_expense(amount, description)
        remaining = cat.remaining_budget()
        print(f"✅ Expense added! Remaining budget for {category_name}: {remaining:.2f}")
        if remaining < 0:
            print(f"⚠ Warning: You are over the {category_name} budget by {-remaining:.2f}!")

    def category_summary(self):
        summary = {}
        for name, cat in self.categories.items():
            summary[name] = {
                "spent": cat.total_spent(),
                "remaining": cat.remaining_budget(),
                "over_budget": cat.is_over_budget()
            }
        return summary

    def display_summary(self):
        print("\n--- Budget Summary ---")
        for name, data in self.category_summary().items():
            status = "⚠ Over Budget!" if data['over_budget'] else "✔ Within Budget"
            print(f"{name}: Spent {data['spent']:.2f} / {self.categories[name].allocation:.2f} → {status}")

    def view_expenses(self, category_name):
        cat = self.categories[category_name]
        balances = cat.running_balances()
        if not balances:
            print(f"\nNo expenses recorded in {category_name}.")
        else:
            print(f"\nExpenses for {category_name} with Running Balance:")
            for i, (desc, amt, remaining) in enumerate(balances, 1):
                print(f"{i}. {desc}: {amt:.2f} | Remaining Budget: {remaining:.2f}")

    def plot_budget(self):
        labels = []
        actual = []
        colors = []

        light_colors = {"Needs": "#FF9999", "Wants": "#ADD8E6", "Savings": "#FFFF99"}
        dark_colors = {"Needs": "#FF4C4C", "Wants": "#3399FF", "Savings": "#FFD633"}

        for name, cat in self.categories.items():
            labels.append(f"{name} ({cat.total_spent():.0f}/{cat.allocation:.0f})")
            actual.append(cat.total_spent())
            colors.append(dark_colors[name] if cat.is_over_budget() else light_colors[name])

        plt.figure(figsize=(6,6))
        plt.pie(actual, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title("Actual Spending vs Recommended Budget (50/30/20 Rule)")
        plt.show()

    def export_csv(self):
        filename = f"Budget_{datetime.now().strftime('%Y-%m-%d')}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Description", "Amount", "Remaining Budget"])
            for name, cat in self.categories.items():
                remaining = cat.allocation
                for desc, amt in cat.expenses:
                    remaining -= amt
                    writer.writerow([name, desc if desc else "No description", amt, remaining])
        print(f"\n✅ Expenses exported successfully to '{filename}'")

# --- Input Validation Functions ---
def get_float_input(prompt):
    while True:
        value = input(prompt)
        try:
            value = float(value)
            if value < 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_option_input(prompt, options):
    options_str = "/".join(options)
    while True:
        value = input(f"{prompt} ({options_str}): ").title()
        if value in options:
            return value
        else:
            print(f"Invalid choice. Please enter one of the following: {options_str}")

# --- Main Program ---
def main():
    print("Welcome to the 50/30/20 Personal Budget Tracker Pro!")

    salary = get_float_input("Enter your monthly take-home salary: ")
    tracker = BudgetTracker(salary)

    while True:
        print("\nOptions:")
        print("1. Add Expense")
        print("2. Show Budget Summary")
        print("3. Show Pie Chart")
        print("4. View Expenses by Category with Running Balance")
        print("5. Export Expenses to CSV")
        print("6. Exit")

        choice = get_option_input("Enter choice", ["1","2","3","4","5","6"])

        if choice == '1':
            category = get_option_input("Enter category", ["Needs","Wants","Savings"])
            amount = get_float_input("Enter expense amount: ")
            description = input("Enter description (optional): ")
            tracker.add_expense(category, amount, description)
        elif choice == '2':
            tracker.display_summary()
        elif choice == '3':
            tracker.plot_budget()
        elif choice == '4':
            category = get_option_input("Select category to view", ["Needs","Wants","Savings"])
            tracker.view_expenses(category)
        elif choice == '5':
            tracker.export_csv()
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    main()