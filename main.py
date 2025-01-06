from re import A
import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
import sqlite3
import os
import sys
from variables import *
from customer import *
from admin import *


# common variables

#font
font_normal=('Arial', 15, 'normal')
font_normal_bold=('Arial', 15, 'bold')
font_small=('Arial', 10, 'normal')
font_small_bold=('Arial', 10, 'bold')

#color
bg_normal= "#BDEDFF"
bg_label = "#EBF4FA"
fc_label = "#123456"
bg_entry = "#FFFFFF"
fc_entry = "#000000"
fg_button = "#24344f"
bg_button = "#FFFFFF"

#size
normal_geo = "520x300"
list_geo = "1920x1080"

#set database
db=sqlite3.connect("bookstore.db")

#cards: table to hold the credit/debit card information
db.execute('''CREATE TABLE IF NOT EXISTS cards(
                   user_id TEXT PRIMARY KEY,
                   name TEXT,
                   cardnumber TEXT,
                   exp_month TEXT,
                   exp_year TEXT,
                   bill_street TEXT,
                   bill_city TEXT,
                   bill_state TEXT,
                   bill_country TEXT,
                   bill_zip TEXT,
                   bill_phone TEXT)''')
db.commit()

#checks: table to hold the bank check information
db.execute('''CREATE TABLE IF NOT EXISTS checks(
                   user_id TEXT PRIMARY KEY,
                   name TEXT,
                   acctype TEXT,
                   routing TEXT,
                   bankacc TEXT)''')
db.commit()

db.execute('''CREATE TABLE IF NOT EXISTS accounts(
                   user_id TEXT PRIMARY KEY,
                   password TEXT NOT NULL,
                   fname TEXT,
                   lname TEXT,
                   email TEXT,
                   saved_payment INTEGER)''')
#saved_payment:
#0: no data
#1: card
#2: check
#3: cash(on delivery)

db.commit()

#books: table to hold the books information 
db.execute('''CREATE TABLE IF NOT EXISTS books(
                   book_id INTEGER PRIMARY KEY,
                   title TEXT,
                   author TEXT,
                   publisher TEXT,
                   price FLOAT,
                   available INTEGER,
                   sold INTEGER)''')
db.commit()

db.execute('''CREATE TABLE IF NOT EXISTS orders(
                   order_id TEXT PRIMARY KEY NOT NULL,
                   user_id TEXT NOT NULL,
                   booklist TEXT,
                   totalprice FLOAT,
                   shipaddress TEXT,
                   payment TEXT)''')
db.commit()

cursor = db.cursor()
cursor.execute("INSERT OR IGNORE into accounts values ('admin', '-', '-', '-', 'admin@email.com', 0)")
db.commit()
cursor.close()

#LoginGUI: set the Login window's appearance and actions
class LoginGUI:
    def __init__(self):
        #Set the cursor for db
        self.cursor = db.cursor()

        #Set the appearance of main window
        #Title the window
        #Set geometry
        #Set background color
        #Place the window
        self.m_window = create_window(self, "User Login", normal_geo)

        #Create frames
        self.login_window = tkinter.Frame(height = 170, width = 520, bg=bg_normal)
        self.creacc_window = tkinter.Frame(height = 170, width = 520, bg=bg_normal)

        #Create labels and entries
        self.login_title = create_title(self.m_window, "WELCOME", 20)

        self.id_label = create_label(self.login_window, "User ID:", 5, 0)
        self.id_entry = create_entry(self.login_window, 190, 0, 20)
        self.pass_label = create_label(self.login_window, "Password:", 5, 30)
        self.pass_entry = create_entry(self.login_window, 190, 30, 20)
        self.pass_entry.configure(show='*')
        self.fname_label = create_label(self.creacc_window, "First Name:", 5, 0)
        self.fname_entry = create_entry(self.creacc_window, 190, 0, 20)
        self.lname_label = create_label(self.creacc_window, "Last Name:", 5, 30)
        self.lname_entry = create_entry(self.creacc_window, 190, 30, 20)
        self.email_label = create_label(self.creacc_window, "Email:", 5, 60)
        self.email_entry = create_entry(self.creacc_window, 190, 60, 20)
        
        #Set the actions on this GUI
        def crelines():
            self.m_window.title("Create New Account")

            self.createlg_button.place_forget()
            self.loginlg_button.place_forget()
            self.creacc_window.place(relx=0.5,y=190,anchor='center')

        def backtologin():

            self.creacc_window.place_forget()
            self.createlg_button.place(x=30, y=70)
            self.loginlg_button.place(x=260, y=70)

        def createacc():
            row=[str(self.id_entry.get()), str(self.pass_entry.get()), str(self.fname_entry.get()), str(self.lname_entry.get()), str(self.email_entry.get()),0]
            self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.id_entry.get()])
            exist = len(self.cursor.fetchall())
            if exist == 0:
                self.cursor.execute('INSERT into accounts values (?,?,?,?,?,?)', row)
                db.commit()
                messagebox.showinfo(title="Created", message= ("Account is created!----- \nUser ID: "+ str(self.id_entry.get())
                                                               + "\nPassword: " + str(self.pass_entry.get())
                                                               + "\nName: " + str(self.fname_entry.get()) + " " + str(self.lname_entry.get())
                                                               + "\nEmail: " + str(self.email_entry.get())
                                                               + "\n------------------------------"
                                                               + "\nNow you can login with these information! Hit 'Login'!"))

                
                backtologin()
                self.m_window.title("User Login")
            else:
                messagebox.showwarning(title="ERROR", message="This User ID has already exists.")
     
        def loginacc():
            self.cursor.execute('SELECT * from accounts WHERE user_id=? AND password=?', [self.id_entry.get(), self.pass_entry.get()])
            exist = len(self.cursor.fetchall())
            if exist == 0:
                messagebox.showwarning(title="ERROR", message= "Invalid User ID or Password")
            elif self.id_entry.get() == 'admin':
                self.m_window.destroy()
                self.cursor.close()
                AdminGUI()
            else:
                user_id = self.id_entry.get()
                self.m_window.destroy()
                self.cursor.close()
                StoreMainGUI(user_id)
                print("it's done")
        
        #Create buttons
        self.createacc_button = create_button_xy(self.creacc_window, "Create Account", createacc, "TButton", 30, 110, 20)
        self.loginacc_button = create_button_xy(self.creacc_window, "Back to Login Screen", backtologin, "TButton", 260, 110, 20)

        self.createacc_button = create_button_xy(self.login_window, "Create New Account", crelines, "TButton", 30, 70, 20)
        self.createacc_button = create_button_xy(self.login_window, "Login", loginacc, "logout.TButton", 260, 70, 20)

        #Loop the window
        self.login_window.place(relx=0.5,y=130,anchor='center')
        self.login_window.mainloop()

#StoremainGUI: set the Store window's appearance and actions
class StoreMainGUI():
    def __init__(self, user_id):
        #Set the cursor for db
        self.user_id = user_id
        self.cursor = db.cursor()

        #Get User Info
        self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.user_id])
        self.userdata = self.cursor.fetchone()
        self.username = (self.userdata[2] + " " + self.userdata[3])

        #Set the appearance of main window
        #Title the window
        #Set geometry
        #Set background color
        #Place the window
        self.store_window = create_window(self, "Store Main", normal_geo)

        #Create labels and entries
        self.store_title = create_title(self.store_window, ("Welcome! %s" %self.username), 40)

        #Set the actions on this GUI
        def buybook():
            self.cursor.close()
            self.store_window.destroy()
            BuyBooksGUI(self.user_id)
            StoreMainGUI(self.user_id)

        def upduserinfo():
            self.cursor.close()
            self.store_window.destroy()
            UserInfoGUI(self, self.user_id)
            StoreMainGUI(self, self.user_id)

        def logout():
            messagebox.showwarning(title="Logout", message="You have been logged out.")
            self.cursor.close()
            self.store_window.destroy()
            LoginGUI()

        #Create buttons
        self.buybook_button = create_button_center(self.store_window, "Buy Books from Book Catalogue", buybook, "TButton", 80, 30)
        self.upduserinfo_button = create_button_center(self.store_window, "Update User Information", upduserinfo, "TButton", 130, 30)
        self.logout_button = create_button_center(self.store_window, "Logout", logout, "logout.TButton", 180, 30)

        #Loop the window
        self.store_window.mainloop()

#AdminGUI: set the admin window's appearance and actions
class AdminGUI():
    def __init__(self):
        #Set the cursor for db
        self.cursor = db.cursor()

        #Set the appearance of main window
        #Title the window
        #Set geometry
        #Set background color
        #Place the window
        self.admin_window = create_window(self, "Admin Main", normal_geo)

        #Create labels and entries
        self.admin_title = create_title(self.admin_window, "Admin Panel", 15)
        #Set the actions on this GUI
        def addbook():
            self.admin_window.destroy()
            self.cursor.close()
            BookManageGUI(False)

        def editbook():
            self.admin_window.destroy()
            self.cursor.close()
            BookManageGUI(True)

        def adduser():
            self.admin_window.destroy()
            self.cursor.close()
            UserManageGUI(False)

        def edituser():
            self.admin_window.destroy()
            self.cursor.close()
            UserManageGUI(True)

        def vieworder():
            self.admin_window.destroy()
            self.cursor.close()
            ViewOrderGUI()

        def logout():
            messagebox.showwarning(title="Logout", message="You have been logged out.")
            self.cursor.close()
            self.admin_window.destroy()
            LoginGUI()

        #Create buttons
        self.adduser_button = create_button_center(self.admin_window, "Save New User Account", adduser, "TButton", 50, 20)
        self.edituser_button = create_button_center(self.admin_window, "Edit User Account", edituser, "TButton", 90, 20)
        self.addbook_button = create_button_center(self.admin_window, "Save New Book", addbook, "TButton", 130, 20)
        self.editbook_button = create_button_center(self.admin_window, "Edit Book", editbook, "TButton", 170, 20)
        self.vieworder_button = create_button_center(self.admin_window, "View Orders", vieworder, "TButton", 210, 20)
        self.logout_button = create_button_center(self.admin_window, "Logout", logout, "logout.TButton", 250, 20)

        #Loop the window
        self.admin_window.mainloop()

if __name__ == "__main__":
    LoginGUI()

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