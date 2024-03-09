from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S
from tkinter import ttk 
from tkinter import messagebox  
from mysql_config import dbconfig
import mysql.connector as pyo
import logging

con = pyo.connect(**dbconfig)

cursor = con.cursor()

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class BookDB:
    def __init__(self):
        self.con = pyo.connect(**dbconfig)
        self.cursor = self.con.cursor()
        print("Connected to the database")
        print(self.con)

    def __del__(self):
        self.con.close()   
    
    def view(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows
    
    def insert(self, title, author, isbn):
        sql = "INSERT INTO books VALUES (NULL, %s, %s, %s)"
        values = [title, author, isbn]
        self.cursor.execute(sql, values)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="New book added to database")

    def update(self, id, title, author, isbn):
        t = (title, author, isbn, id)
        self.cursor.execute("UPDATE books SET title=%s, author=%s, isbn=%s WHERE id=%s", t)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book updated in database")

    def delete(self, id):
        self.cursor.execute("DELETE FROM books WHERE id=%s", [id])
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book deleted from database")

db = BookDB()

def get_selected_row(event):
    global selected_tuple
    index = list_box.curselection()[0]
    selected_tuple = list_box.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_tuple[1])
    author_entry.delete(0, 'end')
    author_entry.insert('end', selected_tuple[2])
    isbn_entry.delete(0, 'end')
    isbn_entry.insert('end', selected_tuple[3])

def view_records():
    list_box.delete(0, 'end')
    for row in db.view():
        list_box.insert('end', row)

def add_book():     
    db.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_box.delete(0, 'end')
    list_box.insert('end', (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.commit()

def delete_records():
    db.delete(selected_tuple[0])
    con.commit()

def clear_screen():
    list_box.delete(0, 'end')
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')

def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.commit()

def on_closing():
    dd = BookDB()
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd
    
root = Tk()  # Creates application window

root.title("My book Database Application")  # Title of the application window
root.configure(background="light blue")  # Background color of the application window
root.geometry("900x500")  # Size of the application window
root.resizable(width=False, height=False)  # Prevent the application window from resizing   

title_label = ttk.Label(root, text="Title", background="light blue", font=("TkDefaultFont",16)) # Create a label
title_label.grid(row=0, column=0, sticky=W) # Position the label in the application window
title_text = StringVar()  # Create a string variable
title_entry = ttk.Entry(root, width=24, textvariable=title_text)  # Create an entry box
title_entry.grid(row=0, column=1, sticky=W)  # Position the entry box in the application window

author_label = ttk.Label(root, text="Author", background="light blue", font=("TkDefaultFont",16))  # Create a label
author_label.grid(row=0, column=2, sticky=W)  # Position the label in the application window
author_text = StringVar()  # Create a string variable
author_entry = ttk.Entry(root, width=24, textvariable=author_text)  # Create an entry box
author_entry.grid(row=0, column=3, sticky=W)  # Position the entry box in the application window

isbn_label = ttk.Label(root, text="ISBN", background="light blue", font=("TkDefaultFont",16))  # Create a label
isbn_label.grid(row=0, column=4, sticky=W)  # Position the label in the application window
isbn_text = StringVar()  # Create a string variable
isbn_entry = ttk.Entry(root, width=24, textvariable=isbn_text)  # Create an entry box
isbn_entry.grid(row=0, column=5, sticky=W)  # Position the entry box in the application window

add_btn = Button(root, text="Add book", bg="green", fg="white", font="helvetica 10 bold", command = add_book)  # Create a button
add_btn.grid(row=0, column=6, sticky=W)  # Position the button in the application window

list_box = Listbox(root, height=16, width=40, font="helvetica 13", bg="light yellow")  # Create a listbox
list_box.grid(row=3, column=1, columnspan=14, sticky=W + E, pady=40, padx=20)  # Position the listbox in the application window
list_box.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)  # Create a scrollbar
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)  # Position the scrollbar in the application window

list_box.configure(yscrollcommand=scroll_bar.set)  # Configure the listbox to use the scrollbar
scroll_bar.configure(command=list_box.yview)  # Configure the scrollbar to move the listbox view

modify_btn = Button(root, text="Modify record", bg="purple", fg="white", font="helvetica 10 bold", command=update_records)  # Create a button
modify_btn.grid(row=15, column=4)  # Position the button in the application window

delete_btn = Button(root, text="Delete record", bg="red", fg="white", font="helvetica 10 bold",command=delete_records)  # Create a button
delete_btn.grid(row=15, column=5)  # Position the button in the application window

view_btn = Button(root, text="View all records", bg="black", fg="white", font="helvetica 10 bold", command = view_records)  # Create a button
view_btn.grid(row=15, column=1)  # Position the button in the application window

clear_btn = Button(root, text="Clear screen", bg="blue", fg="white", font="helvetica 10 bold", command = clear_screen)  # Create a button
clear_btn.grid(row=15, column=2)  # Position the button in the application window

exit_btn = Button(root, text="Exit application", bg="black", fg="white", font="helvetica 10 bold", command = root.destroy)  # Create a button
exit_btn.grid(row=15, column=3)  # Position the button in the application window

root.mainloop()  # Start the application