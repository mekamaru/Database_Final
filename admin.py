from re import A
import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
import sqlite3
import os
from variables import *

class BookManageGUI:

    def __init__(self, flag):

        self.flag = flag
        #Set the cursor for db
        self.cursor = db.cursor()

        #Set the actions on this GUI
        def addbook():
            row = [self.title_entry.get(), self.author_entry.get(), self.publisher_entry.get(), self.price_entry.get(), self.available_entry.get(), 0]
            self.cursor.execute('INSERT into books (title, author, publisher, price, available,sold) values (?,?,?,?,?,?)', row)
            db.commit()
            messagebox.showinfo(title="Save", message= ("Book is saved!----- \nTitle: " + str(self.title_entry.get())
                                                           + "\nAuthor: " + str(self.author_entry.get())
                                                           + "\nPublisher: " + str(self.publisher_entry.get())
                                                           + "\nPrice: " + str(self.price_entry.get())
                                                           + "\nAvailability: " + str(self.available_entry.get())
                                                           + "\n------------------------------"))
            self.book_window.destroy()

        def editbook():
            row = [self.title_entry.get(), self.author_entry.get(), self.publisher_entry.get(), self.price_entry.get(), self.available_entry.get(), self.bookid]
            self.cursor.execute('UPDATE books SET title=?, author=?, publisher=?, price=?, available=? WHERE book_id=?', row)
            db.commit()
            messagebox.showinfo(title="Save", message= ("Book is updated!----- \nBook ID: "+ str(self.bookid)
                                                           + "\nTitle: " + str(self.title_entry.get())
                                                           + "\nAuthor: " + str(self.author_entry.get())
                                                           + "\nPublisher: " + str(self.publisher_entry.get())
                                                           + "\nPrice: " + str(self.price_entry.get())
                                                           + "\nAvailability: " + str(self.available_entry.get())
                                                           + "\n------------------------------"))
            self.book_window.destroy()
            setlist()

        def deletebook():
            messagebox.showinfo(title="Save", message= ("Book is deleted!----- \nBook ID: "+ str(self.bookid)
                                                           + "\nTitle: " + str(self.title_entry.get())
                                                           + "\nAuthor: " + str(self.author_entry.get())
                                                           + "\nPublisher: " + str(self.publisher_entry.get())
                                                           + "\nPrice: " + str(self.price_entry.get())
                                                           + "\nAvailability: " + str(self.available_entry.get())
                                                           + "\n------------------------------"))
            self.cursor.execute('DELETE from books WHERE book_id=?', [self.bookid,])
            db.commit()
            self.book_window.destroy()
            setlist()

        def getbookinfo(book_id):
            self.book_window.geometry(normal_geo)
            self.cursor.execute('SELECT * FROM books WHERE book_id=?', [book_id, ])

            self.bookinfo = self.cursor.fetchone()
                    
            self.title_entry.insert(0, self.bookinfo[1])
            self.author_entry.insert(0, self.bookinfo[2])
            self.publisher_entry.insert(0, self.bookinfo[3])
            self.price_entry.insert(0, self.bookinfo[4])
            self.available_entry.delete(0)
            self.available_entry.insert(0, self.bookinfo[5])
            self.bookid = book_id
            placelines(editbook,"Update Book Info")

        def placelines(command, text):
            self.book_window.geometry(normal_geo)
            self.save_button = ttk.Button(self.book_window, command = command, text = text, style="TButton", width=20)
            self.title_label.place(x=5, y=30)
            self.author_label.place(x=5, y=60)
            self.publisher_label.place(x=5, y=90)
            self.price_label.place(x=5, y=120)
            self.available_label.place(x=5, y=150)
            
            self.title_entry.place(x=110, y=30)
            self.author_entry.place(x=110, y=60)
            self.publisher_entry.place(x=110, y=90)
            self.price_entry.place(x=110, y=120)
            self.available_entry.place(x=110, y=150)
            self.save_button.place(x=30, y=190)

            if flag == True:
                self.delete_button.place(x=260, y=190)
                self.back_button.place(x=150, y=230)

            else:
                self.cancel_button.place(x=260, y=190)

        def cancel():
            self.book_window.destroy()
            from main import AdminGUI
            AdminGUI()

        def back():
            self.book_window.destroy()
            setlist()

        def setlist():
            #Set the appearance of main window
            #Title the window
            #Set geometry
            #Set background color
            #Place the window
            self.book_window = create_window(self, "Manage Book Catalogue", list_geo)
    
            #Create labels and entries
            # Creating a label and entry box for Title
            self.title_label = tkinter.Label(self.book_window, text="Title:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.title_entry = tkinter.Entry(self.book_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=30)
            
            # Creating a label and entry box for Author
            self.author_label = tkinter.Label(self.book_window, text="Author:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.author_entry = tkinter.Entry(self.book_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=30)    

            # Creating a label and entry box for Publisher
            self.publisher_label = tkinter.Label(self.book_window, text="Publisher:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.publisher_entry = tkinter.Entry(self.book_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=30)

            # Creating a label and entry box for Price
            self.price_label = tkinter.Label(self.book_window, text="Price:      $", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.price_entry = tkinter.Entry(self.book_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label and entry box for Available
            self.available_label = tkinter.Label(self.book_window, text="Available:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.available_entry = tkinter.Spinbox(self.book_window, from_=0, to = 2147483647, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        
            #Create buttons
            self.cancel_button = ttk.Button(self.book_window, command=cancel, text="Cancel", style="TButton", width=20)
            self.back_button = ttk.Button(self.book_window, command=back, text="Back", style="TButton", width=20)
            self.delete_button = ttk.Button(self.book_window, command = deletebook, text = "Delete the Book", style="TButton", width=20)
            

            if flag == True: #edit book
                
                #Create scrollable canvas
                self.editbook_title = create_title(self.book_window, "Choose a book for edit", 20)
                self.cancel_button.lift()
                self.cancel_button.place(relx = 0.5, y=760, anchor = 'center')
                self.cursor.execute('SELECT * FROM books')
                book_list = self.cursor.fetchall()
                book_id = create_scroll(self.book_window, 680, 1000, 30, 420, book_list,"book")
                print("bookid: " + str(book_id))
                self.editbook_title.destroy()
                getbookinfo(book_id)

            else: #add new book
                placelines(addbook, "Save New Book")
    
            #Loop the window
            self.book_window.mainloop()

        setlist()

class UserManageGUI:

    def __init__(self, flag):

        self.flag = flag
        #Set the cursor for db
        self.cursor = db.cursor()

        #Set the actions on this GUI
        def adduser():
            if self.userid_entry.get() == '':
                messagebox.showwarning(title="ERROR", message="User ID is not given")
            else:
                self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.userid_entry.get()])
                exist = len(self.cursor.fetchall())
                if exist == 0:
                    row = [self.userid_entry.get(), self.pass_entry.get(), self.fname_entry.get(), self.lname_entry.get(), self.email_entry.get(), 0]
                    self.cursor.execute('INSERT into accounts (user_id, password, fname, lname, email, saved_payment) values (?,?,?,?,?,?)', row)
                    db.commit()
                    messagebox.showinfo(title="Save", message= ("User is saved!----- \nUser ID: "+ str(self.userid_entry.get())
                                                                   + "\nPassword: " + str(self.pass_entry.get())
                                                                   + "\nFirstname: " + str(self.fname_entry.get())
                                                                   + "\nLastname: " + str(self.lname_entry.get())
                                                                   + "\nEmail: " + str(self.email_entry.get())
                                                                   + "\n------------------------------"))
                    self.acc_window.destroy()
                    adminGUI()
                else:
                    messagebox.showwarning(title="ERROR", message="This User ID has already exists.")

        def edituser():
            row = [self.pass_entry.get(), self.fname_entry.get(), self.lname_entry.get(), self.email_entry.get(), self.saved_payment_entry.get(), self.user_id]
            self.cursor.execute('UPDATE accounts SET password=?, fname=?, lname=?, email=?, saved_payment=? WHERE user_id=?', row)
            db.commit()
            messagebox.showinfo(title="Save", message= ("User is updated!----- \nUser ID: "+ str(self.user_id)
                                                           + "\nPassword: " + str(self.pass_entry.get())
                                                           + "\nFirstname: " + str(self.fname_entry.get())
                                                           + "\nLastname: " + str(self.lname_entry.get())
                                                           + "\nEmail: " + str(self.email_entry.get())
                                                           + "\nPayment method: " + str(self.saved_payment_entry.get())
                                                           + "\n------------------------------"))
            self.acc_window.destroy()
            setlist()

        def deleteuser():
            self.cursor.execute('DELETE from accounts WHERE user_id=?', [self.user_id,])
            db.commit()
            messagebox.showinfo(title="Delete", message= ("User Account for '%s' is deleted." %str(self.user_id)))
            self.acc_window.destroy()
            setlist()

        def getuserinfo(user_id):
            print("user_id: %s"%str(user_id))
            self.acc_window.geometry(normal_geo)
            self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [user_id, ])

            self.userinfo = self.cursor.fetchone()
                    
            self.pass_entry.insert(0, self.userinfo[1])
            self.fname_entry.insert(0, self.userinfo[2])
            self.lname_entry.insert(0, self.userinfo[3])
            self.email_entry.insert(0, self.userinfo[4])
            self.saved_payment_entry.insert(0, self.userinfo[5])
            self.userid = user_id
            placelines(edituser,"Update User Info")

        def placelines(command, text):
            self.acc_window.geometry(normal_geo)
            self.save_button = ttk.Button(self.acc_window, command = command, text = text, style="TButton", width=20)

            if flag == True:
                self.pass_label.place(x=5, y=30)
                self.fname_label.place(x=5, y=60)
                self.lname_label.place(x=5, y=90)
                self.email_label.place(x=5, y=120)
                self.saved_payment_label.place(x=5, y=150)
                self.method_label.place(x=5, y=180)
                
                self.pass_entry.place(x=200, y=30)
                self.fname_entry.place(x=200, y=60)
                self.lname_entry.place(x=200, y=90)
                self.email_entry.place(x=200, y=120)
                self.saved_payment_entry.place(x=200, y=150)
            
                self.save_button.place(x=30, y=220)
                self.delete_button.place(x=260, y=220)
                self.back_button.place(x=150, y=250)

            else:
                self.userid_label.place(x=5, y=30)
                self.pass_label.place(x=5, y=60)
                self.fname_label.place(x=5, y=90)
                self.lname_label.place(x=5, y=120)
                self.email_label.place(x=5, y=150)

                self.userid_entry.place(x=200, y=30)
                self.pass_entry.place(x=200, y=60)
                self.fname_entry.place(x=200, y=90)
                self.lname_entry.place(x=200, y=120)
                self.email_entry.place(x=200, y=150)
                self.save_button.place(x=30, y=220)
                self.cancel_button.place(x=260, y=220)

        def cancel():
            self.acc_window.destroy()
            from main import AdminGUI
            AdminGUI()

        def back():
            self.acc_window.destroy()
            setlist()

        def setlist():
            #Set the appearance of main window
            #Title the window
            #Set geometry
            #Set background color
            #Place the window
            self.acc_window = create_window(self, "Manage Accounts", list_geo)
    
            #Create labels and entries
            self.method_label = tkinter.Label(self.acc_window, text="1: Card/2: Check/3: Cash/0: None", font=font_normal_bold, fg=fc_label, bg=bg_normal)

            # Creating a label for User ID
            self.userid_label = tkinter.Label(self.acc_window, text="User ID:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.userid_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label for Password
            self.pass_label = tkinter.Label(self.acc_window, text="Password:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.pass_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
            
            # Creating a label for First Name
            self.fname_label = tkinter.Label(self.acc_window, text="First Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.fname_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label for Last Name
            self.lname_label = tkinter.Label(self.acc_window, text="Last Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.lname_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
                
            # Creating a label for Email
            self.email_label = tkinter.Label(self.acc_window, text="Email:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.email_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label for Payment Method
            self.saved_payment_label = tkinter.Label(self.acc_window, text="Payment method:", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.saved_payment_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        
            #Create buttons
            self.cancel_button = ttk.Button(self.acc_window, command=cancel, text="Cancel", style="TButton", width=20)
            self.back_button = ttk.Button(self.acc_window, command=back, text="Back", style="TButton", width=20)
            self.delete_button = ttk.Button(self.acc_window, command = deleteuser, text = "Delete the Book", style="TButton", width=20)
            

            if flag == True: #edit user
                
                #Create scrollable canvas
                self.edituser_title = create_title(self.acc_window, "Choose an account for edit", 20)
                self.cancel_button.lift()
                self.cancel_button.place(relx = 0.5, y=760, anchor = 'center')
                self.cursor.execute('SELECT * FROM accounts')
                user_list = self.cursor.fetchall()
                user_id = create_scroll(self.acc_window, 680, 1000, 30, 420, user_list,"user")
                self.edituser_title.destroy()
                getuserinfo(user_id)

            else: #add new user
                placelines(adduser, "Save New User")
    
            #Loop the window
            self.acc_window.mainloop()

        setlist()
def ViewOrderGUI(self):
    print("This is ViewOrderGUI")

    #Set the cursor for db
    #self.cursor = db.cursor()
    
    #Get User Info
    
    #Set the appearance of main window
    #Title the window
    #Set geometry
    #Set background color
    #Place the window
    
    #Set style
    
    #Create frames
    
    #Create labels and entries
    
    #Set the actions on this GUI
    
    #Create buttons
    
    #Loop the window