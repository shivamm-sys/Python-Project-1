import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

BOOKS_FILE = "books.csv"
ISSUED_FILE = "issued_books.csv"
USER_LOG_FILE = "user_log.csv"
FINE_PER_DAY = 2  # INR or USD per day late

# Initialize CSVs
def init_files():
    for file, columns in [(BOOKS_FILE, ["Book_ID", "Title", "Author", "Copies"]),
                          (ISSUED_FILE, ["Book_ID", "User", "Issue_Date", "Due_Date"]),
                          (USER_LOG_FILE, ["User", "Book_ID", "Action", "Date", "Fine"])]:
        try:
            pd.read_csv(file)
        except FileNotFoundError:
            pd.DataFrame(columns=columns).to_csv(file, index=False)

# Add a book
def add_book():
    book_id = input("Book ID: ")
    title = input("Title: ")
    author = input("Author: ")
    copies = int(input("Number of Copies: "))

    books = pd.read_csv(BOOKS_FILE)
    books = pd.concat([books, pd.DataFrame([[book_id, title, author, copies]],
                                           columns=books.columns)], ignore_index=True)
    books.to_csv(BOOKS_FILE, index=False)
    print(" Book added!")

# List all books
def list_books():
    books = pd.read_csv(BOOKS_FILE)
    print("\n Book Inventory:\n", books)

# Issue a book
def issue_book():
    book_id = input("Book ID to issue: ")
    user = input("User name: ")
    books = pd.read_csv(BOOKS_FILE)
    book = books[books['Book_ID'] == book_id]

    if book.empty or int(book.iloc[0]['Copies']) <= 0:
        print(" Book not available.")
        return

    books.loc[books['Book_ID'] == book_id, 'Copies'] -= 1
    books.to_csv(BOOKS_FILE, index=False)

    issue_date = datetime.today()
    due_date = issue_date + timedelta(days=14)
    issued = pd.read_csv(ISSUED_FILE)
    issued = pd.concat([issued, pd.DataFrame([[book_id, user, issue_date.strftime('%Y-%m-%d'), due_date.strftime('%Y-%m-%d')]],
                                             columns=issued.columns)], ignore_index=True)
    issued.to_csv(ISSUED_FILE, index=False)

    log_action(user, book_id, "Issue", issue_date.strftime('%Y-%m-%d'), 0)
    print(" Book issued until", due_date.date())

# Return a book
def return_book():
    book_id = input("Book ID to return: ")
    user = input("User name: ")
    issued = pd.read_csv(ISSUED_FILE)
    books = pd.read_csv(BOOKS_FILE)

    match = issued[(issued['Book_ID'] == book_id) & (issued['User'] == user)]
    if match.empty:
        print(" No matching issued book found.")
        return

    due_date = datetime.strptime(match.iloc[0]['Due_Date'], '%Y-%m-%d')
    return_date = datetime.today()
    days_late = (return_date - due_date).days
    fine = max(0, days_late * FINE_PER_DAY)

    # Remove from issued
    issued = issued.drop(match.index)
    issued.to_csv(ISSUED_FILE, index=False)

    # Add copy back
    books.loc[books['Book_ID'] == book_id, 'Copies'] += 1
    books.to_csv(BOOKS_FILE, index=False)

    log_action(user, book_id, "Return", return_date.strftime('%Y-%m-%d'), fine)
    print(f" Book returned! Fine: ₹{fine}" if fine else " Book returned on time.")

# Log action
def log_action(user, book_id, action, date, fine):
    log = pd.read_csv(USER_LOG_FILE)
    new_entry = pd.DataFrame([[user, book_id, action, date, fine]], columns=log.columns)
    log = pd.concat([log, new_entry], ignore_index=True)
    log.to_csv(USER_LOG_FILE, index=False)

# View usage chart
def most_borrowed_chart():
    log = pd.read_csv(USER_LOG_FILE)
    borrowed = log[log['Action'] == "Issue"]
    top = borrowed['Book_ID'].value_counts().head(5)

    if top.empty:
        print(" No borrow data available.")
        return

    plt.figure(figsize=(8, 5))
    top.plot(kind='bar', color='skyblue')
    plt.title(" Most Borrowed Books")
    plt.ylabel("Times Borrowed")
    plt.xlabel("Book ID")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

# Export user log
def export_logs():
    log = pd.read_csv(USER_LOG_FILE)
    export_path = "exported_user_log.csv"
    log.to_csv(export_path, index=False)
    print(f" User log exported to {export_path}")

# Menu
def menu():
    init_files()
    while True:
        print("\n Library System Menu")
        print("1. Add Book")
        print("2. List Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Most Borrowed Books Chart")
        print("6. Export User Log")
        print("7. Exit")

        choice = input("Choose option: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            issue_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            most_borrowed_chart()
        elif choice == '6':
            export_logs()
        elif choice == '7':
            print("Exiting system.")
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    menu()
