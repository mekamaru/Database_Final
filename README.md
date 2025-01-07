Simply Bookstore app for my own practice.
Rewriting bookstore.py.

# Functions
## User
- login with user own account: `LoginGUI()` → `StoreMainGUI()`
- create an account for the user: `LoginGUI()`
- edit the user's account: `StoreMainGUI()` → `UserInfoGUI()`
- buy books: `StoreMainGUI()` → `BuyBooksGUI()`
- logout: → `LoginGUI()`

## Admin
- login with admin account: `LoginGUI()` → `AdminGUI()`
- create account for a user: `AdminGUI()` → `UserManageGUI(False)`
- edit users' accounts: `AdminGUI()` → `UserManageGUI(True)`
- register new book info: `AdminGUI()` → `BookManageGUI(False)`
- edit books' info: `AdminGUI()` → `BookManageGUI(True)`
- view orders: `AdminGUI()` → `ViewOrderGUI()`
- logout: → `LoginGUI()`

# Files
## main.py
- Control the entire functions
- Create account
- Login
### class
- `LoginGUI()`
- `StoreMainGUI()`
- `AdminGUI()`
### database
- `accounts`

## customer.py
- User's functions
  - login with own user account: `LoginGUI()` → `StoreMainGUI()`
  - create an account for the user: `LoginGUI()`
  - edit the user's account: `StoreMainGUI()` → `UserInfoGUI()`
  - buy books: `StoreMainGUI()` → `BuyBooksGUI()`
  - logout: → `LoginGUI()`
### class
- `BuyBooksGUI()`
- `UserInfoGUI()`
### database
- `accounts`
- `books`
- `cards`
- `checks`
- `orders`

## admin.py
- Admin's functions
  - login with admin account: `LoginGUI()` → `AdminGUI()`
  - create account for a user: `AdminGUI()` → `UserManageGUI(False)`
  - edit users' accounts: `AdminGUI()` → `UserManageGUI(True)`
  - register new book info: `AdminGUI()` → `BookManageGUI(False)`
  - edit books' info: `AdminGUI()` → `BookManageGUI(True)`
  - view orders: `AdminGUI()` → `ViewOrderGUI()`
  - logout: → `LoginGUI()`
### class
- `UserManageGUI()`
- `BookManageGUI()`
- `ViewOrderGUI()`
### database
- `accounts`
- `books`
- `cards`
- `checks`
- `orders`

## variables.py
- common variables and functions like header file for C++
### database
- `accounts`
- `books`

# Databases
## accounts
- user_id: text
  - User ID
  - **primary key**
- password: text NOT null
  - Password
- fname: text
  - First Name
- lname: text
  - Last Name
- email: text
  - Email
- saved_payment: int
  - Saved Payment Method
    - 1: Credit/Debit card
    - 2: Check
    - 3: Cash (on delivery)
    - 0: None or Unsaved

## books
- book_id: int
  - Book ID
  - **primary key**
- title: text
  - Book title
- author: text
  - Book's author
- publisher: text
  - Book's publisher
- price: float
  - Book's price($)
- available: int
  - Quantity of the book in stock
- sold: int
  - Number of sales of the book
 
## orders
- order_id: text NOT null
  - Order ID
  - **primary key**
- user_id: text NOT null
  - User ID
- booklist: text
  - List of purchased books
- totalprice: float
  - Total amount paid 
- shipaddress: text
  - Shipping address (appended) 
- payment: text
  - Payment method

## cards
- user_id: text
  - User ID
  - **primary key**
- name: text
  - Name on the card
- cardnumber: text
  - card number
- exp_month: text
  - expire month of the card
- exp_year: text
  - expire year of the card
- bill_street: text
  - street info of billing address
- bill_city: text
  - city info of billing address
- bill_state: text
  - state info of billing address 
- bill_country: text
  - country info of billing address
- bill_zip: text
  - Zip code info of billing address   
- bill_phone: text
  - Phone number registered in the card

## checks
- user_id: text
  - User ID
  - **primary key**
- name: text
  - Bank name
- acctype: text
  - Account type
    - Checking
    - Saving 
- routing: text
  - Routing Number
- bankacc: text
  - Account Number
