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

## variables.py
- common variables and functions like header file for C++

