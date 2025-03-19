import mysql.connector
import tkinter as tk
from tkinter import messagebox

class Library:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='', database='library_db')
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            book_id VARCHAR(10) PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            issued BOOLEAN DEFAULT FALSE
        )''')
        self.conn.commit()
    
    def add_book(self, book_id, title, author):
        try:
            self.cursor.execute("INSERT INTO books (book_id, title, author) VALUES (%s, %s, %s)", (book_id, title, author))
            self.conn.commit()
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))
    
    def display_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        return books
    
    def issue_book(self, book_id):
        self.cursor.execute("SELECT issued FROM books WHERE book_id = %s", (book_id,))
        result = self.cursor.fetchone()
        if result:
            if result[0]:
                messagebox.showwarning("Warning", "Book is already issued!")
            else:
                self.cursor.execute("UPDATE books SET issued = TRUE WHERE book_id = %s", (book_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
        else:
            messagebox.showerror("Error", "Book ID not found!")
    
    def return_book(self, book_id):
        self.cursor.execute("SELECT issued FROM books WHERE book_id = %s", (book_id,))
        result = self.cursor.fetchone()
        if result:
            if result[0]:
                self.cursor.execute("UPDATE books SET issued = FALSE WHERE book_id = %s", (book_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Book returned successfully!")
            else:
                messagebox.showwarning("Warning", "Book was not issued!")
        else:
            messagebox.showerror("Error", "Book ID not found!")
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Library Management System", font=("Arial", 16)).pack()
        
        tk.Button(self.root, text="Add Book", command=self.add_book_window).pack(pady=5)
        tk.Button(self.root, text="View Books", command=self.view_books).pack(pady=5)
        tk.Button(self.root, text="Issue Book", command=self.issue_book_window).pack(pady=5)
        tk.Button(self.root, text="Return Book", command=self.return_book_window).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)
    
    def add_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Book")
        
        tk.Label(window, text="Book ID:").pack()
        book_id_entry = tk.Entry(window)
        book_id_entry.pack()
        
        tk.Label(window, text="Title:").pack()
        title_entry = tk.Entry(window)
        title_entry.pack()
        
        tk.Label(window, text="Author:").pack()
        author_entry = tk.Entry(window)
        author_entry.pack()
        
        def submit():
            self.library.add_book(book_id_entry.get(), title_entry.get(), author_entry.get())
            window.destroy()
        
        tk.Button(window, text="Add", command=submit).pack()
    
    def view_books(self):
        window = tk.Toplevel(self.root)
        window.title("Available Books")
        
        books = self.library.display_books()
        for book in books:
            status = 'Issued' if book[3] else 'Available'
            tk.Label(window, text=f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}").pack()
    
    def issue_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Issue Book")
        
        tk.Label(window, text="Enter Book ID:").pack()
        book_id_entry = tk.Entry(window)
        book_id_entry.pack()
        
        def submit():
            self.library.issue_book(book_id_entry.get())
            window.destroy()
        
        tk.Button(window, text="Issue", command=submit).pack()
    
    def return_book_window(self):
        window = tk.Toplevel(self.root)
        window.title("Return Book")
        
        tk.Label(window, text="Enter Book ID:").pack()
        book_id_entry = tk.Entry(window)
        book_id_entry.pack()
        
        def submit():
            self.library.return_book(book_id_entry.get())
            window.destroy()
        
        tk.Button(window, text="Return", command=submit).pack()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
