import tkinter as tk
from tkinter import ttk
import json
import os
import datetime as dt
from datetime import datetime
import sys

class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = int(isbn)
        self.quantity = int(quantity)

    def display_details(self):
        return f"Title: {self.title}\n Author: {self.author}\n ISBN: {self.isbn}\n Quantity: {self.quantity}"


class Patron:
    def __init__(self, name, patron_id, contact_info):
        self.name = name
        self.patron_id = patron_id
        self.contact_info = contact_info

    def display_details(self):
        return f"Name: {self.name} , Patron ID: {self.patron_id} , Contact Info: {self.contact_info}"


class Transaction:
    def __init__(self, book, patron, due_date, fine):
        self.book = book
        self.patron = patron
        self.due_date = None
        self.fine = 0


class Library:
    def __init__(self):
        self.books = []  # List of Book objects
        self.patrons = []  # List of Patron objects
        self.transactions = []

    def search_books(self, keyword):
        matching_books = []
        for book in self.books:
            if keyword.lower() == book.title.lower() or keyword.lower() == book.author.lower() or keyword == book.isbn:
                matching_books.append(book)
        return matching_books
    def save_to_json(self, filename):
        data = {
            "books": [book.__dict__ for book in self.books],
            "patrons": [patron.__dict__ for patron in self.patrons],
            "transactions": [transaction.__dict__ for transaction in self.transactions]
        }
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def load_from_json(self, filename):
        if os.path.isfile(filename):  # Check if the file exists
            with open(filename, "r") as json_file:
                data = json.load(json_file)
                self.books = [Book(**book) for book in data.get("books", [])]
                self.patrons = [Patron(**patron) for patron in data.get("patrons", [])]
                self.transactions = [Transaction(**transaction) for transaction in data.get("transactions", [])]
        else:
            print(f"The file {filename} does not exist. Creating a new JSON file.")
            default_data = {
                "books": [],
                "patrons": [],
                "transactions": []
            }
            with open(filename, "w") as json_file:
                json.dump(default_data, json_file, indent=4)
            print(f"A new JSON file '{filename}' has been created with default data.")


class LibraryApp(Library):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Library Management System")

        self.library = Library()
        self.library.load_from_json("library_data.json")

        # Create a menu
        self.menu_label = tk.Label(self.root, text="Select an option:")
        self.menu_label.pack()

        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        # Create a canvas to hold the buttons
        self.canvas = tk.Canvas(self.scrollable_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(fill="both", expand=True)

        # Configure the scrollbar to work with the canvas
        self.scrollbar.config(command=self.canvas.yview)

        # Create a frame inside the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.admin_button = tk.Button(self.inner_frame, text="Librarian & Admin", command=self.admin_access)
        self.admin_button.pack()

        self.user_button = tk.Button(self.inner_frame, text="User", command=self.user_access)
        self.user_button.pack()

    def remove_widgets(self):
        try:
            for item in self.clear_book:
                item.destroy()
        except:
            pass
        try:
            self.result_text.destroy()
        except:
            pass
        try:
            for item in self.clear_search1:
                item.destroy()
        except:
            pass
        try:
            for item in self.clear_transaction:
                item.destroy()
        except:
            pass
        try:
            for item in self.clear_patron:
                item.destroy()
        except:
            pass
        try:
            self.result_text2.destroy()
        except:
            pass

    def rerun_program(self):
        root.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def admin_access(self):

        self.manage_books_button = tk.Button(self.inner_frame, text="Manage Books", command=self.manage_books)
        self.manage_books_button.pack()

        self.manage_patrons_button = tk.Button(self.inner_frame, text="Manage Patrons", command=self.manage_patrons)
        self.manage_patrons_button.pack()

        self.handle_transactions_button = tk.Button(self.inner_frame, text="Handle Transactions", command=self.transaction_input)
        self.handle_transactions_button.pack()

        self.search_books_button = tk.Button(self.inner_frame, text="Search Books", command=self.searching_books)
        self.search_books_button.pack()

        self.report_button = tk.Button(self.inner_frame, text="Generate Report", command=self.generate_report)
        self.report_button.pack()

        self.rerun_button = tk.Button(root, text="Rerun Program", command=self.rerun_program)
        self.rerun_button.pack(pady=10)

        self.user_button.destroy()
        self.admin_button.destroy()

    def user_access(self):

        self.handle_transactions_button = tk.Button(self.inner_frame, text="Handle Transactions", command=self.transaction_input)
        self.handle_transactions_button.pack()

        self.search_books_button = tk.Button(self.inner_frame, text="Search Books", command=self.searching_books)
        self.search_books_button.pack()

        self.rerun_button = tk.Button(root, text="Rerun Program", command=self.rerun_program)
        self.rerun_button.pack(pady=10)

        self.user_button.destroy()
        self.admin_button.destroy()

    def generate_report(self):

        self.remove_widgets()

        with open('library_data.json', 'r') as json_file:
            json_object = json.load(json_file)

        print(json.dumps(json_object, indent=1))

        for items in self.transactions:
            print(self.transactions)

        self.result_text2 = tk.Text(self.inner_frame, height=2, width=50)
        self.result_text2.pack()

        self.result_text2.delete(1.0, tk.END)
        self.result_text2.insert(tk.END, f"Report Generated")

        self.clear_report = [self.result_text2]

    def manage_patrons(self):
        self.remove_widgets()

        self.manage_patrons_label = tk.Label(self.inner_frame, text="Add or Remove Patrons")
        self.manage_patrons_label.pack()

        self.name_entry = tk.Entry(self.inner_frame, width=30)
        self.name_entry.insert(0, "Name")  # Placeholder text
        self.name_entry.bind("<FocusIn>", self.clear_placeholder2)
        self.name_entry.pack()

        self.id_entry = tk.Entry(self.inner_frame, width=30)
        self.id_entry.insert(0, "ID")  # Placeholder text
        self.id_entry.bind("<FocusIn>", self.clear_placeholder2)
        self.id_entry.pack()

        self.contactinfo_entry = tk.Entry(self.inner_frame, width=30)
        self.contactinfo_entry.insert(0, "Contact Info")  # Placeholder text
        self.contactinfo_entry.bind("<FocusIn>", self.clear_placeholder2)
        self.contactinfo_entry.pack()

        self.remove_patron_button = tk.Button(self.inner_frame, text="Remove", command=self.remove_patron)
        self.remove_patron_button.pack()

        self.add_patron_button = tk.Button(self.inner_frame, text="Add", command=self.add_patron)
        self.add_patron_button.pack()

        self.clear_patron = [self.manage_patrons_label,self.name_entry,self.id_entry,self.contactinfo_entry,self.remove_patron_button,self.add_patron_button]
    def clear_placeholder2(self, event):
        if self.name_entry.get() == "Name":
            self.name_entry.delete(0, tk.END)
        if self.id_entry.get() == "ID":
            self.id_entry.delete(0, tk.END)
        if self.contactinfo_entry.get() == "Contact Info":
            self.contactinfo_entry.delete(0, tk.END)

    def add_patron(self):

        name = self.name_entry.get()
        id = self.id_entry.get()
        contact = self.contactinfo_entry.get()

        if id not in [patron.patron_id for patron in self.library.patrons]:
            new_patron = Patron(name, id, contact)
            self.library.patrons.append(new_patron)
            print(f"Added new patron: \n {new_patron.display_details()}")
        else:
            print("user has already been registered")

        self.library.save_to_json("library_data.json")

        # Clear the entry fields
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.contactinfo_entry.delete(0, tk.END)

    def remove_patron(self):

        name = self.name_entry.get()
        id = self.id_entry.get()
        contact = self.contactinfo_entry.get()

        matching_patron = [patron for patron in self.library.patrons if
                           patron.name.lower() == name.lower() and
                           patron.patron_id.lower() == id.lower() and
                           patron.contact_info.lower() == contact.lower()]

        if matching_patron:
            removed_patron = matching_patron[0]
            self.library.patrons.remove(removed_patron)
            self.library.save_to_json("library_data.json")
            print(f"Removed patron: {removed_patron.display_details()}")
        else:
            print(f"No patron found with the specified details.")

        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.contactinfo_entry.delete(0, tk.END)


    def transaction_input(self):
        self.remove_widgets()

        self.transac = tk.Label(self.inner_frame, text="Search for Transaction")
        self.transac.pack()

        self.book = tk.Entry(self.inner_frame, width=30)
        self.book.insert(0, "Book")  # Placeholder text
        self.book.bind("<FocusIn>", self.clear_placeholder3)
        self.book.pack()

        self.name = tk.Entry(self.inner_frame, width=30)
        self.name.insert(0, "Name")  # Placeholder text
        self.name.bind("<FocusIn>", self.clear_placeholder3)
        self.name.pack()

        self.transac_button = tk.Button(self.inner_frame, text="Check Out", command=self.handle_transactions)
        self.transac_button.pack()

        self.return_button = tk.Button(self.inner_frame, text="Return Book", command=self.return_book)
        self.return_button.pack()

        self.clear_transaction = [self.transac,self.book,self.name,self.transac_button,self.return_button]

    def clear_placeholder3(self, event):
        if self.name.get() == "Name":
            self.name.delete(0, tk.END)
        if self.book.get() == "Book":
            self.book.delete(0, tk.END)


    def handle_transactions(self):
        book = self.book.get()
        patron = self.name.get()
        fine = 0

        book_exists = False
        for available_book in self.library.books:
            if available_book.title == book and available_book.quantity > 0:
                book_exists = True
                break

        if book_exists:
            due_date = dt.date.today() + dt.timedelta(days=14)
            transaction = Transaction(book, patron, str(due_date), fine)
            available_book.quantity -= 1
            self.library.transactions.append(transaction)
            self.library.save_to_json("library_data.json")
            print(f"Book '{book}' checked out by {patron}. Due date: {due_date}")
        else:
            print(f"Book '{book}' is not available for checkout.")

    def return_book(self):
        book = self.book.get()
        patron = self.name.get()

        for available_book in self.library.books:
            pass


        for transaction in self.library.transactions:
            if transaction.book == book and transaction.patron == patron:
                if transaction.due_date is not None:  # Check if due_date is not None
                    time_calc = dt.datetime.strptime(transaction.due_date, "%Y-%m-%d").date()
                    if dt.date.today() > time_calc:
                        days_late = (dt.date.today() - time_calc).days
                        transaction.fine = days_late * 2
                available_book.quantity += 1
                self.library.transactions.remove(transaction)
                self.library.save_to_json("library_data.json")
                print(f"Book '{book}' returned by {patron}. Fine: ${transaction.fine}")
                break
        else:
            print(f"Book '{book}' was not checked out by {patron}.")

    def searching_books(self):
        self.remove_widgets()

        self.search_entry = tk.Entry(self.inner_frame)
        self.search_entry.pack()
        self.search_button = tk.Button(self.inner_frame, text="Search", command=self.search_books)
        self.search_button.pack()

        self.clear_search1 = [self.search_entry,self.search_button]

    def search_books(self):
        try:
            self.result_text.destroy()
        except:
            pass

        keyword = self.search_entry.get()

        matching_books = self.library.search_books(keyword)

        self.result_text = tk.Text(self.inner_frame, height=4, width=50)
        self.result_text.pack()
        if matching_books:
            self.result_text.delete(1.0, tk.END)
            for book in matching_books:
                self.result_text.insert(tk.END, book.display_details())
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"No books found for '{keyword}'.")

    def manage_books(self):
        self.remove_widgets()

        # Add Book Form
        self.add_book_label = tk.Label(self.inner_frame, text="Add or Remove Books")
        self.add_book_label.pack()

        self.title_entry = tk.Entry(self.inner_frame, width=30)
        self.title_entry.insert(0, "Title")  # Placeholder text
        self.title_entry.bind("<FocusIn>", self.clear_placeholder)
        self.title_entry.pack()

        self.author_entry = tk.Entry(self.inner_frame, width=30)
        self.author_entry.insert(0, "Author")  # Placeholder text
        self.author_entry.bind("<FocusIn>", self.clear_placeholder)
        self.author_entry.pack()

        self.isbn_entry = tk.Entry(self.inner_frame, width=30)
        self.isbn_entry.insert(0, "ISBN")  # Placeholder text
        self.isbn_entry.bind("<FocusIn>", self.clear_placeholder)
        self.isbn_entry.pack()

        self.quantity_entry = tk.Entry(self.inner_frame, width=30)
        self.quantity_entry.insert(0, "Quantity")  # Placeholder text
        self.quantity_entry.bind("<FocusIn>", self.clear_placeholder)
        self.quantity_entry.pack()

        self.remove_book_button = tk.Button(self.inner_frame, text="Remove", command=self.remove_book)
        self.remove_book_button.pack()

        self.add_book_button = tk.Button(self.inner_frame, text="Add", command=self.add_book)
        self.add_book_button.pack()

        self.clear_book = [self.add_book_label,self.title_entry,self.author_entry,self.isbn_entry,self.quantity_entry,self.remove_book_button,self.add_book_button]

    def clear_placeholder(self, event):
        if self.title_entry.get() == "Title":
            self.title_entry.delete(0, tk.END)
        if self.author_entry.get() == "Author":
            self.author_entry.delete(0, tk.END)
        if self.isbn_entry.get() == "ISBN":
            self.isbn_entry.delete(0, tk.END)
        if self.quantity_entry.get() == "Quantity":
            self.quantity_entry.delete(0, tk.END)

    def add_book(self):

        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        quantity = self.quantity_entry.get()

        if isbn not in [book.isbn for book in self.library.books]:
            new_book = Book(title, author, isbn, quantity)
            self.library.books.append(new_book)
            print(f"Added new book: \n {new_book.display_details()}")
        else:
            print("book has already been registered")

        self.library.save_to_json("library_data.json")

        # Clear the entry fields
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def remove_book(self):

        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        quantity = self.quantity_entry.get()

        matching_books = [book for book in self.library.books if
                          book.title.lower() == title.lower() and
                          book.author.lower() == author.lower() and
                          book.isbn.lower() == isbn.lower() and book.quantity == quantity]

        if matching_books:
            removed_book = matching_books[0]
            self.library.books.remove(removed_book)
            self.library.save_to_json("library_data.json")
            print(f"Removed book: {removed_book.display_details()}")
        else:
            print(f"No book found with the specified details.")

        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

    # Save library data to JSON file
    app.library.save_to_json("library_data.json")