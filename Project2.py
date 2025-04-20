import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = 'expenses.csv'

# Here we Initialize file
def init_file():
    try:
        pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
        df.to_csv(CSV_FILE, index=False)

# Add an expense
def add_expense():
    date_input = input("Date (YYYY-MM-DD) [default: today]: ")
    date = date_input if date_input else datetime.today().strftime('%Y-%m-%d')
    category = input("Category (e.g., Food, Transport): ")
    amount = float(input("Amount: "))
    note = input("Note (optional): ")

    new_expense = pd.DataFrame([[date, category, amount, note]],
                               columns=["Date", "Category", "Amount", "Note"])
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    print("Expense added!")

# Weekly or Monthly summary
def generate_summary(period="monthly"):
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])

    if period == "weekly":
        df['Week'] = df['Date'].dt.to_period('W')
        summary = df.groupby(['Week', 'Category'])['Amount'].sum().unstack().fillna(0)
    else:
        df['Month'] = df['Date'].dt.to_period('M')
        summary = df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)

    print(f"\n {period.capitalize()} Summary:\n")
    print(summary.round(2))

# Visualize with Matplotlib & NumPy
def plot_expenses():
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    monthly = df.groupby(['Month', 'Category'])['Amount'].sum().unstack().fillna(0)

    # Convert PeriodIndex to strings for plotting
    months = monthly.index.astype(str)
    categories = monthly.columns
    data = monthly.to_numpy()

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(10, 6))

    # Stack bars
    bottom = np.zeros(len(months))
    for i, category in enumerate(categories):
        ax.bar(x, data[:, i], bottom=bottom, label=category)
        bottom += data[:, i]

    ax.set_title(" Monthly Expenses by Category")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.show()

# Main Menu
def main():
    init_file()
    while True:
        print("\n Expense Tracker")
        print("1. Add Expense")
        print("2. Weekly Summary")
        print("3. Monthly Summary")
        print("4. Visualize Expenses")
        print("5. Exit")

        choice = input("Choose option: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            generate_summary("weekly")
        elif choice == '3':
            generate_summary("monthly")
        elif choice == '4':
            plot_expenses()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
