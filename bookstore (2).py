
from re import A
import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
import sqlite3
import os


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
    #def __init__(self)
     #Set the cursor for db

     #Set the appearance of main window
        #Title the window
        #Set geometry
        #Set background color
        #Set style
        #Place the window

     #Create frames

     #Create labels and entries

     #Create buttons

     #Set the actions on this GUI

     #Loop the window
     

#StoremainGUI: set the Store window's appearance and actions
class StoremainGUI():
    #def __init__(self)
     #Set the cursor for db

     #Set the appearance of main window
        #Title the window
        #Set geometry
        #Set background color
        #Set style
        #Place the window

     #Create frames

     #Create labels and entries

     #Create buttons

     #Set the actions on this GUI

     #Loop the window

#BuyBooksGUI: set the BuyBooks window's appearance and actions
class BuyBooksGUI():

#UserInfoGUI: set the userinfo window's appearance and actions
class UserInfoGUI():


#AdminGUI: set the admin window's appearance and actions
class AdminGUI():

#UserManageGUI: set the user manage window (for admin)'s appearance and actions
class UserManageGUI():

#BookManageGUI: set the book manage window (for admin)'s appearance and actions
class BookManageGUI():

#ViewOrderGUI(): set the view orders window (for admin)'s appearace and actions
class ViewOrderGUI():
 
LoginGUI()
