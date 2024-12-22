
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

#loginGUI: set the Login window's appearance and actions
class loginGUI:

    def __init__(self):

    #Set the apperance of basic screen
        self.m_window = tkinter.Tk()
        #Title of the application
        self.m_window.title("User Login")

        #Geometry string is a standard way of describing the size and location of the window
        # Set the size of the window (x and  y position of the root window)
        self.m_window.geometry(normal_geo)
        self.m_window.config(bg=bg_normal) #Background color

        self.login_window = tkinter.Frame(height = 170, width = 520, bg=bg_normal)
        self.creacc_window = tkinter.Frame(height = 170, width = 520, bg=bg_normal)

        
        self.cursor = db.cursor()

        def crelines():
            self.m_window.title("Create New Account")

            self.login_window.place_forget()
            self.creacc_window.place(x=0,y=130)

        def backtologin():

            self.creacc_window.place_forget()
            self.login_window.place(x=0,y=130)
            
    #Set the actions
        #insert() : user input data -> save it in database
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

        #delete() : user input data -> delete it from database
        def loginacc():
            self.cursor.execute('SELECT * from accounts WHERE user_id=? AND password=?', [self.id_entry.get(), self.pass_entry.get()])
            exist = len(self.cursor.fetchall())
            if exist == 0:
                messagebox.showwarning(title="ERROR", message= "Invalid User ID or Password")
            elif self.id_entry.get() == 'admin':
                self.m_window.destroy()
                self.cursor.close()
                adminGUI()
            else:
                user_id = self.id_entry.get()
                self.m_window.destroy()
                self.cursor.close()
                storemainGUI(user_id)
                
                
    #Set the appearance of login window
        self.welcome = tkinter.Label(self.m_window, text="WELCOME", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.welcome.place(x=200, y=10)

        # Creating a label for User ID
        self.id_label = tkinter.Label(self.m_window, text="User ID:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.id_label.place(x=5, y=70)

        # Creating a text entry box for User ID
        self.id_entry = tkinter.Entry(self.m_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        self.id_entry.place(x=190, y=70)

        # Creating a label for Password
        self.pass_label = tkinter.Label(self.m_window, text="Password:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.pass_label.place(x=5, y=100)

        # Creating a text entry box for Password
        self.pass_entry = tkinter.Entry(self.m_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, show="*", width=20)
        self.pass_entry.place(x=190, y=100)

        # Creating a label for First Name
        self.fname_label = tkinter.Label(self.creacc_window, text="First Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.fname_label.place(x=5, y=0)
            
        # Creating a text entry box for First Name
        self.fname_entry = tkinter.Entry(self.creacc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        self.fname_entry.place(x=190, y=0)

        # Creating a label for Last Name
        self.lname_label = tkinter.Label(self.creacc_window, text="Last Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.lname_label.place(x=5, y=30)

        # Creating a text entry box for Last Name
        self.lname_entry = tkinter.Entry(self.creacc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        self.lname_entry.place(x=190, y=30)
            
        # Creating a label for Email
        self.email_label = tkinter.Label(self.creacc_window, text="Email:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.email_label.place(x=5, y=60)
            
        # Creating a text entry box for Email
        self.email_entry = tkinter.Entry(self.creacc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        self.email_entry.place(x=190, y=60)

        # Creating the buttons
        self.createacc_button = ttk.Button(self.creacc_window, command=createacc, text="Create Account", style="TButton", width=20)
        self.createacc_button.place(x=30, y=110)
        self.loginacc_button = ttk.Button(self.creacc_window, command=backtologin, text="Back to Login Screen", style="TButton", width=20)
        self.loginacc_button.place(x=260, y=110)

        self.createlg_button = ttk.Button(self.login_window, command=crelines, text="Create New Account", style="TButton", width=20)
        self.createlg_button.place(x=30, y=40)
        self.loginlg_button = ttk.Button(self.login_window, command=loginacc, text="Login", style="TButton", width=20)
        self.loginlg_button.place(x=260, y=40)

        self.login_window.place(x=0,y=130)

        self.style = ttk.Style()
        self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        

        # Loop the window
        self.login_window.mainloop()


#storemainGUI: set the Store window's appearance and actions
class storemainGUI():

    def __init__(self, user_id):
        self.user_id = user_id
        self.cursor = db.cursor()

    #Set the appearance
        self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.user_id])
        self.userdata = self.cursor.fetchone()
        self.username = (self.userdata[2] + " " + self.userdata[3])
        print("Welcome! " + self.username)

        self.store_window = tkinter.Tk()
        self.store_window.title("Store Main")
        #Geometry string is a standard way of describing the size and location of the window
        # Set the size of the window (x and  y position of the root window)
        self.store_window.geometry(normal_geo)
        self.store_window.config(bg=bg_normal)

    #Set the actions
        def buybook():
            self.cursor.close()
            self.store_window.destroy()
            BuyBooksGUI(self.user_id)

        def upduserinfo():
            self.cursor.close()
            self.store_window.destroy()
            UserInfoGUI(self.user_id)

        def logout():
            messagebox.showwarning(title="Logout", message="You have been logged out.")
            self.cursor.close()
            self.store_window.destroy()
            loginGUI()

    #Set the detail appearance of buttons
        self.welcome_label = tkinter.Label(self.store_window, text=("Welcome! %s" %self.username), font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.welcome_label.place(x=150, y=40)
        self.buybook_button = ttk.Button(self.store_window, command=buybook, text="Buy Books from Book Catalogue", style="TButton", width=30)
        self.buybook_button.place(x=95, y=80)
        self.upduserinfo_button = ttk.Button(self.store_window, command=upduserinfo, text="Update User Information", style="TButton", width=30)
        self.upduserinfo_button.place(x=95, y=130)
        self.logout_button = ttk.Button(self.store_window, command=logout, text="Logout", style="TButton", width=30)
        self.logout_button.place(x=95, y=180)


        self.style = ttk.Style()
        self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)

    #Loop the window
        self.store_window.mainloop()

        #storemainGUI()に呼び出されるGUIは全部user_idを参照する。
        #bookcatalogue一覧から選ぶ -> 選択画面がメインウィンドウのGUI(user_id)
            #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）
            #カタログのフィルタリング →第二フレーム
            #合計金額の計算　→　第三フレーム
        #選択一覧　→　オーバーレイフレームその①
            #合計金額　→　function
            #選択一覧からカタログに戻れる必要がある　→　選択一覧.place_forget()
        #会計　→　オーバーレイフレームその②
            #支払い方法の選択　↑
                #支払い方法の入力　→　オーバーｒｙその③
                    #支払い方法の保存　→　function
        #購入履歴の保存
            #bookのsoldとavailableのアップデート
            #accountのsaved_paymentのアップデート
            #ordersに追加

        #アカウント情報の変更
            #user_id以外は全部
            #saved_paymentは一から変更の恐れ
        #過去の購入履歴の確認
            #履歴のフィルタリング

#BuyBooksGUI: set the BuyBooks window's appearance and actions
class BuyBooksGUI():
    def __init__(self, user_id): #storemainGUI()に呼び出されるGUIは全部user_idを参照する。
        self.user_id = user_id
        self.cursor = db.cursor()

    #Set the appearance
        self.selectbook_window = tkinter.Tk() #bookcatalogue一覧から選ぶ -> 選択画面がメインウィンドウのGUI(user_id)
        self.selectbook_window.title("Order Books [User ID: %s]" %self.user_id)
        self.selectbook_window.geometry("820x500")
        h = 500
        w = 820
        self.bgcolor = bg_normal
        self.bgcolor2 = "#AFDCEC"
        self.selectbook_window.config(bg = self.bgcolor) 

        self.selectbook_window_mid = tkinter.Frame(height = 125, width = w, bg = self.bgcolor) #カタログのフィルタリング →第二フレーム
        self.selectbook_window_bot = tkinter.Frame(height = 175, width = w, bg = self.bgcolor) #合計金額の計算　→　第三フレーム
        self.purchase_window_top = tkinter.Frame(height = 30, width = w, bg = self.bgcolor) #会計　→　オーバーレイフレームその②
        self.purchase_window_bot = tkinter.Frame(height = 300, width = w, bg = self.bgcolor) #会計　→　オーバーレイフレームその②
        self.method_window_main = tkinter.Frame(height = h, width = w, bg = self.bgcolor) #支払い方法の入力　→　オーバーｒｙその③
        self.method_window_card = tkinter.Frame(height = 300, width = w, bg = self.bgcolor2)
        self.method_window_cash = tkinter.Frame(height = 150, width = w, bg = self.bgcolor2)
        self.method_window_bank = tkinter.Frame(height = 300, width = w, bg = self.bgcolor2)

        self.canvas = tkinter.Canvas(self.selectbook_window, bg =self.bgcolor, height = 275, width= w) #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）

        # Scrollbar を生成して配置
        self.bar = tkinter.Scrollbar(self.selectbook_window, orient=tkinter.VERTICAL)
        
        self.bar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.bar.set)
        

        # Frame Widgetを 生成
        #frame = tkinter.Frame(canvas,height = 200, width = w, bg = bg_label) #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）

        # Frame Widgetを Canvas Widget上に配置

        maxid = self.cursor.execute('SELECT Max(book_id) FROM books').fetchone()[0]
        maxprice = self.cursor.execute('SELECT Max(price) FROM books').fetchone()[0]
        maxavailable = self.cursor.execute('SELECT Max(available) FROM books').fetchone()[0]
        if maxid != None:
            self.orderbooks = [0]* (maxid + 1)
        else: self.orderbooks = [0]
        if maxprice == None:
            maxprice = 0
        if maxavailable == None:
            maxavailable = 0
        self.subtotal = 0
        self.qtytotal = 0

    #Set the actions
        def cancel():
            self.cursor.close()
            self.selectbook_window.destroy()
            storemainGUI(self.user_id)
        

        def calctotalprice():
            self.subtotal = 0
            self.qtytotal = 0
            for i in range(0, len(self.listofbooks)):
                if int(self.numberofbooks[i].get()) > self.listofbooks[i][5]:
                    messagebox.showwarning(title = "ERROR", message = (self.listofbooks[i][1] + " is added more than available number of books"))
                else:
                    self.subtotal = (float(self.priceofbooks[i]) * int(self.numberofbooks[i].get())) + self.subtotal
                    self.qtytotal = int(self.numberofbooks[i].get()) + self.qtytotal
                    self.total_head.place_forget()
                    self.total_head = tkinter.Label(self.selectbook_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(round(self.subtotal, 2))), font=font_normal_bold, fg=fc_label, bg=bg_label)
                    self.total_head.place(x=300, y=10)
                    self.orderbooks[self.listofbooks[i][0]] = self.numberofbooks[i].get()
                    
            

        # 複数の Button Widget 生成し、Frame上に配置 = スクロールして本を選ぶという動作を成立させる
        
        self.listofbooks = []
        self.priceofbooks = []
        self.numberofbooks = []
        def createbookslist(conn):
            self.listofbooks = []
            self.priceofbooks = []
            self.numberofbooks = []
            self.bookcatalogue = tkinter.Frame(self.canvas,height = 200, width = w, bg = bg_label)

            self.canvas.config(height = 275)
            self.canvas.create_window((0,0), window=self.bookcatalogue, anchor=tkinter.NW, width=self.canvas.cget('width'))
            selectedbooks = conn.fetchall()
            self.canvas.config(scrollregion=(0,0,50,len(selectedbooks)*30)) #スクロール範囲
            title_head = tkinter.Label(self.bookcatalogue, text= "Title", font=font_small, fg=fc_label, bg=bg_label)
            title_head.grid(row = 0, column = 1)
            author_head = tkinter.Label(self.bookcatalogue, text= "Author", font=font_small, fg=fc_label, bg=bg_label)
            author_head.grid(row = 0, column = 2)
            publisher_head = tkinter.Label(self.bookcatalogue, text= "Publisher", font=font_small, fg=fc_label, bg=bg_label)
            publisher_head.grid(row = 0, column = 3)
            price_head = tkinter.Label(self.bookcatalogue, text= "Price", font=font_small, fg=fc_label, bg=bg_label)
            price_head.grid(row = 0, column = 4)
            available_head = tkinter.Label(self.bookcatalogue, text= "Availablity", font=font_small, fg=fc_label, bg=bg_label)
            available_head.grid(row = 0, column = 5)
            qty_head = tkinter.Label(self.bookcatalogue, text= "Qty", font=font_small, fg=fc_label, bg=bg_label)
            qty_head.grid(row = 0, column = 6)
            
            for bk in selectedbooks:
                self.listofbooks.append(bk)
                var = tkinter.DoubleVar()
                title = tkinter.Label(self.bookcatalogue, text= str(bk[1]), font=font_small, fg=fc_label, bg=bg_label)
                author = tkinter.Label(self.bookcatalogue, text= str(bk[2]), font=font_small, fg=fc_label, bg=bg_label)
                publisher = tkinter.Label(self.bookcatalogue, text= str(bk[3]), font=font_small, fg=fc_label, bg=bg_label)
                price = tkinter.Label(self.bookcatalogue, text= ("$" + str(bk[4])), font=font_small, fg=fc_label, bg=bg_label)
                available = tkinter.Label(self.bookcatalogue, text= str(bk[5]), font=font_small, fg=fc_label, bg=bg_label)
                unavailable = tkinter.Label(self.bookcatalogue, text= "Unavailable", font=font_small, fg=fc_label, bg=bg_label)
                numofbk = tkinter.Spinbox(self.bookcatalogue, from_=0, to=bk[5], width = 20, command = calctotalprice)
                numofbk.configure(width = 5)
                numofbk.delete(0)
                if self.orderbooks[bk[0]] != 0:
                    numofbk.insert(0, int(self.orderbooks[bk[0]]))
                else:
                    numofbk.insert(0,0)
                self.priceofbooks.append(bk[4])
                self.numberofbooks.append(numofbk)
                title.grid(row = len(self.priceofbooks) + 1, column = 1, sticky = tkinter.W)
                author.grid(row = len(self.priceofbooks) + 1, column = 2, sticky = tkinter.W)
                publisher.grid(row = len(self.priceofbooks) + 1, column = 3, sticky = tkinter.W)
                price.grid(row = len(self.priceofbooks) + 1, column = 4, sticky = tkinter.W)
                available.grid(row = len(self.priceofbooks) + 1, column = 5)
                if bk[5] != 0:
                    numofbk.grid(row = len(self.priceofbooks) + 1, column=6)
                else:
                    unavailable.grid(row = len(self.priceofbooks) + 1, column=6)

            self.bar.pack(side=tkinter.RIGHT, pady=120, ipady =158, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 125)

        createbookslist(self.cursor.execute('SELECT * FROM books'))
        
        

        def filterbooks():
            def is_positivenum(n):
                try:
                    float(n)
                except ValueError:
                    return False
                else:
                    if float(n) < 0:
                        return False
                    else:
                        return True
                
            if self.price_min_entry.get() == "" or is_positivenum(self.price_min_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Minimum price is empty or invalid input"))
            elif self.price_max_entry.get() == "" or is_positivenum(self.price_max_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Maximum price is empty or invalid input"))
            elif self.available_min_entry.get() == "" or is_positivenum(self.available_min_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Minimum available is empty or invalid input"))
            elif self.available_max_entry.get() == "" or is_positivenum(self.available_max_entry.get()) == False:
                messagebox.showwarning(title = "ERROR", message = ("Maximum available is empty or invalid input"))
            elif self.price_min_entry.get() > self.price_max_entry.get():
                messagebox.showwarning(title = "ERROR", message = ("Minimum price is greater than Maximum price"))
            elif self.available_min_entry.get() > self.available_max_entry.get():
                messagebox.showwarning(title = "ERROR", message = ("Minimum avilable is greater than Maximum available"))
            else:
                self.bookcatalogue.destroy()
                row = [("%" + self.title_entry.get() + "%"), ("%" + self.author_entry.get() + "%"),("%" + self.publisher_entry.get() + "%"),
                       self.price_min_entry.get(), self.price_max_entry.get(), self.available_min_entry.get(), self.available_max_entry.get()]
                self.listofbooks = []
                self.priceofbooks = []
                self.numberofbooks = []
                createbookslist(self.cursor.execute('SELECT * FROM books WHERE \
                                                    title LIKE ? AND\
                                                    author LIKE ? AND\
                                                    publisher LIKE ? AND\
                                                    ? <= price AND price <= ? AND\
                                                    ? <= available AND available <= ?',
                                                    row))
        def filterreset():
            if len(self.title_entry.get()) != 0: self.title_entry.delete(0, len(self.title_entry.get()))
            if len(self.author_entry.get()) != 0: self.author_entry.delete(0, len(self.author_entry.get()))
            if len(self.publisher_entry.get()) != 0: self.publisher_entry.delete(0, len(self.publisher_entry.get()))
            
            if len(self.price_min_entry.get()) != 0: self.price_min_entry.delete(0, len(self.price_min_entry.get()))
            self.price_min_entry.insert(0, int(0))
            if len(self.price_max_entry.get()) != 0: self.price_max_entry.delete(0, len(self.price_max_entry.get()))
            self.price_max_entry.insert(0, maxprice)
            
            if len(self.available_min_entry.get()) != 0: self.available_min_entry.delete(0, len(self.available_min_entry.get()))
            self.available_min_entry.insert(0, int(0))
            if len(self.available_max_entry.get()) != 0: self.available_max_entry.delete(0, len(self.available_max_entry.get()))
            self.available_max_entry.insert(0, maxavailable)

        def cartreset():
            maxid = self.cursor.execute('SELECT Max(book_id) FROM books').fetchone()[0]
            if maxid != None:
                self.orderbooks = [0]* (maxid + 1)
            else: self.orderbooks = [0]
            self.qtytotal = 0
            self.subtotal = 0
            self.total_head.destroy()
            self.bookcatalogue.destroy()
            self.total_head = tkinter.Label(self.selectbook_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(self.subtotal)),
                                            font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.total_head.place(x=300, y=10)
            createbookslist(self.cursor.execute('SELECT * FROM books'))
            
            

        def backtoCatalogue():
            self.purchase_window_top.place_forget()
            self.purchase_window_bot.place_forget()
            self.bkcatalogue_summary.destroy()
            self.selectbook_window_mid.place(x = 0, y = 0)
            self.selectbook_window_bot.place(x = 0, y = 375)
            self.total_head_summary.place_forget()
            self.subandtax.place_forget()
            self.taxtotal.place_forget()
            self.bar.pack(side=tkinter.RIGHT, pady=120, ipady =158, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 125)
            createbookslist(self.cursor.execute('SELECT * FROM books'))
            filterreset()

        def is_invalid(n):
            try:
                int(n)
            except ValueError:
                return True
            else:
                if int(n) < 0:
                    return True
                else:
                    return False

        self.method = "None"
        self.payinfo = []

        def selectpayment():
            
            def gotopay():
                self.pay_method = tkinter.Label(self.purchase_window_bot, text=self.method, font=font_small, fg=fc_label, bg=bg_label)
                self.pay_method.place(x=135, y=210)
                print(self.savecheck.get())
                print(self.payinfo)
                self.method_window_main.place_forget()
                self.method_window_cash.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_card.place_forget()
                self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
                self.canvas.pack(side=tkinter.TOP, pady = 35)

            def backtosum():
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_main.place_forget()
                self.method_window_cash.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_card.place_forget()
                self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
                self.canvas.pack(side=tkinter.TOP, pady = 35)
                
            def card():
                def savecard():
                    if self.cardname_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Name on Card is empty"))
                    elif self.cardnumber_entry.get() == "" or is_invalid(self.cardnumber_entry.get()) or len(self.cardnumber_entry.get())!=16:
                        messagebox.showwarning(title = "ERROR", message = ("Card Number is empty or invalid input"))
                    elif self.cardcvc_entry.get() == "" or is_invalid(self.cardcvc_entry.get()) or len(self.cardcvc_entry.get())!=3:
                        messagebox.showwarning(title = "ERROR", message = ("Card CVC is empty or invalid input"))
                    elif self.cardexpmon_entry.get() == "" or is_invalid(self.cardexpmon_entry.get()) or len(self.cardexpmon_entry.get())!=2:
                        messagebox.showwarning(title = "ERROR", message = ("Card Exp Month is empty or invalid input"))
                    elif int(self.cardexpmon_entry.get()) > 12:
                        messagebox.showwarning(title = "ERROR", message = ("Card Exp Month is invalid input"))
                    elif self.cardexpyear_entry.get() == "" or is_invalid(self.cardexpyear_entry.get()) or len(self.cardexpyear_entry.get())!=2:
                        messagebox.showwarning(title = "ERROR", message = ("Card Exp Year is empty or invalid input"))
                    elif self.bill_street_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: Street is empty or invalid input"))
                    elif self.bill_city_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: City is empty or invalid input"))
                    elif self.bill_state_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: State is empty or invalid input"))
                    elif self.bill_country_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: Country is empty or invalid input"))
                    elif self.bill_zip_entry.get() == "" or is_invalid(self.bill_zip_entry.get()) or len(self.bill_zip_entry.get())<5:
                        messagebox.showwarning(title = "ERROR", message = ("Billing Address: Zip Code is empty or invalid input"))
                    elif self.cardphone_entry.get() == "" or is_invalid(self.bill_zip_entry.get()):
                        messagebox.showwarning(title = "ERROR", message = ("Phone number is empty or invalid input"))
                    else:
                        self.payinfo = [self.user_id, str(self.cardname_entry.get()), str(self.cardnumber_entry.get()),
                                        str(self.cardexpmon_entry.get()), str(self.cardexpyear_entry.get()), str(self.bill_street_entry.get()),
                                        str(self.bill_city_entry.get()), str(self.bill_state_entry.get()), str(self.bill_country_entry.get()),
                                        str(self.bill_zip_entry.get()), str(self.cardphone_entry.get())]
                        gotopay()
                    
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_cash.place_forget()
                self.method_window_bank.place_forget()
                self.method = "Credit/Debit Card"

                self.card_selectpay_head = tkinter.Label(self.method_window_card, text="Card Information", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.card_selectpay_head.place(x=350, y=5)

                self.cardinfo_head = tkinter.Label(self.method_window_card, text="Card Detail:", font=font_small_bold, fg=fc_label, bg=bg_label)
                self.cardname_label = tkinter.Label(self.method_window_card, text="Name on Card:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardname_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.cardnumber_label = tkinter.Label(self.method_window_card, text="Card Number:", font=font_small, fg=fc_label, bg=bg_label)
                self.nospace = tkinter.Label(self.method_window_card, text = "(no space)", font=font_small, fg=fc_label, bg=bg_label)
                self.cardnumber_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.cardexp_label = tkinter.Label(self.method_window_card, text="Expire MM/YY:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardexpmon_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=3)
                self.cardexpto_label = tkinter.Label(self.method_window_card, text="/", font=font_small, fg=fc_label, bg=self.bgcolor2)
                self.cardexpyear_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=3)
                self.cardcvc_label = tkinter.Label(self.method_window_card, text="CVC:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardcvc_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, show = "*", fg=fc_entry, bg=bg_entry, width=5)
                self.cardphone_label = tkinter.Label(self.method_window_card, text="Phone:", font=font_small, fg=fc_label, bg=bg_label)
                self.cardphone_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)

                
                
                
                self.bill_head = tkinter.Label(self.method_window_card, text="Billing Address:", font=font_small_bold, fg=fc_label, bg=bg_label)
                self.bill_street_label = tkinter.Label(self.method_window_card, text="Street:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_street_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_city_label = tkinter.Label(self.method_window_card, text="City:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_city_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_state_label = tkinter.Label(self.method_window_card, text="State:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_state_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_country_label = tkinter.Label(self.method_window_card, text="Country:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_country_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.bill_zip_label = tkinter.Label(self.method_window_card, text="Zipcode:", font=font_small, fg=fc_label, bg=bg_label)
                self.bill_zip_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
                self.card_savemethod_button = tkinter.Checkbutton(self.method_window_card, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 1, offvalue = 0, font = font_small, bg = self.bgcolor2)
                self.card_savemethod_button.deselect()

                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 1:
                    pinfo = self.cursor.execute('SELECT * FROM cards WHERE user_id=?', [self.user_id,]).fetchone()
                    self.cardname_entry.insert(0, pinfo[1])
                    self.cardnumber_entry.insert(0, pinfo[2])
                    self.cardexpmon_entry.insert(0, pinfo[3])
                    self.cardexpyear_entry.insert(0, pinfo[4])
                    self.bill_street_entry.insert(0, pinfo[5])
                    self.bill_city_entry.insert(0, pinfo[6])
                    self.bill_state_entry.insert(0, pinfo[7])
                    self.bill_country_entry.insert(0, pinfo[8])
                    self.bill_zip_entry.insert(0, pinfo[9])
                    self.cardphone_entry.insert(0, pinfo[10])
                    self.card_savemethod_button.select()
                    
                self.cardinfo_head.place(x=20, y=50)
                self.cardname_label.place(x=20, y=70)
                self.cardname_entry.place(x=113, y=71)
                self.cardnumber_label.place(x=20, y=90)
                self.cardnumber_entry.place(x=113, y=91)
                self.nospace.place(x=325, y=90)
                self.cardexp_label.place(x=20, y=110)
                self.cardexpmon_entry.place(x=113, y=111)
                self.cardexpto_label.place(x=138, y=110)
                self.cardexpyear_entry.place(x=148, y=111)
                self.cardcvc_label.place(x=20, y=130)
                self.cardcvc_entry.place(x=113, y=131)
                self.cardphone_label.place(x=20, y=150)
                self.cardphone_entry.place(x=113, y=151)
                
                self.bill_head.place(x=430, y=50)
                self.bill_street_label.place(x=430, y=70)
                self.bill_street_entry.place(x=485, y=71)
                self.bill_city_label.place(x=430, y=90)
                self.bill_city_entry.place(x=485, y=91)
                self.bill_state_label.place(x=430, y=110)
                self.bill_state_entry.place(x=485, y=111)
                self.bill_country_label.place(x=430, y=130)
                self.bill_country_entry.place(x=485, y=131)
                self.bill_zip_label.place(x=430, y=150)
                self.bill_zip_entry.place(x=485, y=151)

                
                
                self.card_savemethod_button.place(x=305, y=180)
                self.savecard_button = ttk.Button(self.method_window_card, command=savecard, text="Save Payment Method", style="TButton", width=30)
                self.savecard_button.place(x=316, y=220)
                self.card_backtosum_button = ttk.Button(self.method_window_card, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
                self.card_backtosum_button.place(x=316, y=250)
                
                self.method_window_card.place(x=0,y=130)

            def bank():
                
                def savebank():
                    if self.bankname_entry.get() == "":
                        messagebox.showwarning(title = "ERROR", message = ("Bank Name is empty"))
                    elif self.banktype.get() == "None":
                        messagebox.showwarning(title = "ERROR", message = ("Account Type is not selected"))
                    elif self.routing_entry.get() == "" or is_invalid(self.routing_entry.get()):
                        messagebox.showwarning(title = "ERROR", message = ("Routing Number is empty or invalid input"))
                    elif self.bankacc_entry.get() == "" or is_invalid(self.bankacc_entry.get()):
                        messagebox.showwarning(title = "ERROR", message = ("Account Number is empty or invalid input"))
                    else:
                        self.payinfo = [self.user_id, (self.bankname_entry.get()), str(self.banktype.get()),
                                        str(self.routing_entry.get()), str(self.bankacc_entry.get())]
                        gotopay()
                    
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_card.place_forget()
                self.method_window_cash.place_forget()
                self.method = "Bank Check"

                self.bank_selectpay_head = tkinter.Label(self.method_window_bank, text="Bank Information", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.bank_selectpay_head.place(x=350, y=5)

                self.bankinfo_head = tkinter.Label(self.method_window_bank, text="Bank Detail:", font=font_small_bold, fg=fc_label, bg=bg_label)
                self.bankname_label = tkinter.Label(self.method_window_bank, text="Bank Name:", font=font_small, fg=fc_label, bg=bg_label)
                self.bankname_entry = tkinter.Entry(self.method_window_bank, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.banktype = tkinter.StringVar(value="None")
                self.banktype_label = tkinter.Label(self.method_window_bank, text="Account Type:", font=font_small, fg=fc_label, bg=bg_label)
                self.banktype_entry = tkinter.OptionMenu(self.method_window_bank, self.banktype, "Checking", "Saving" )
                self.routing_label = tkinter.Label(self.method_window_bank, text="Routing Number:", font=font_small, fg=fc_label, bg=bg_label)
                self.routing_entry = tkinter.Entry(self.method_window_bank, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
                self.bankacc_label = tkinter.Label(self.method_window_bank, text="Account Number:", font=font_small, fg=fc_label, bg=bg_label)
                self.bankacc_entry = tkinter.Entry(self.method_window_bank, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)

                self.bank_savemethod_button = tkinter.Checkbutton(self.method_window_bank, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 2, offvalue = 0, font = font_small, bg = self.bgcolor2)
                self.bank_savemethod_button.deselect()
                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 2:
                    pinfo = self.cursor.execute('SELECT * FROM checks WHERE user_id=?', [self.user_id,]).fetchone()
                    self.bankname_entry.insert(0, pinfo[1])
                    self.banktype = tkinter.StringVar(value=pinfo[2])
                    self.banktype_entry = tkinter.OptionMenu(self.method_window_bank, self.banktype, "Checking", "Saving" )
                    self.routing_entry.insert(0, pinfo[3])
                    self.bankacc_entry.insert(0, pinfo[4])
                    self.bank_savemethod_button.select()


                self.banktype_entry.config(font = font_small)
                self.bankinfo_head.place(x=20, y=50)
                self.bankname_label.place(x=20, y=70)
                self.bankname_entry.place(x=125, y=71)
                self.banktype_label.place(x=20, y=97)
                self.banktype_entry.place(x=125, y=93)
                self.routing_label.place(x=20, y=125)
                self.routing_entry.place(x=125, y=126)
                self.bankacc_label.place(x=20, y=150)
                self.bankacc_entry.place(x=125, y=151)

                
                
                self.bank_savemethod_button.place(x=305, y=180)
                self.savebank_button = ttk.Button(self.method_window_bank, command=savebank, text="Save Payment Method", style="TButton", width=30)
                self.savebank_button.place(x=316, y=220)
                self.bank_backtosum_button = ttk.Button(self.method_window_bank, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
                self.bank_backtosum_button.place(x=316, y=250)
                
                self.method_window_bank.place(x=0,y=130)

            def cash():
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_card.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_cash.place(x=0,y=130)
                self.method = "Cash (on Delivery)"

                self.cash_head = tkinter.Label(self.method_window_cash, text="You must pay when you receive the box.", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.cash_head.place(x=230, y=10)

                self.cash_savemethod_button = tkinter.Checkbutton(self.method_window_cash, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 3, offvalue = 0, font = font_small, bg = self.bgcolor2)
                self.cash_savemethod_button.deselect()

                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 3:
                    self.cash_savemethod_button.select()
                    
                self.cash_savemethod_button.place(x=305, y=40)
                self.savecash_button = ttk.Button(self.method_window_cash, command=gotopay, text="Save Payment Method", style="TButton", width=30)
                self.savecash_button.place(x=316, y=80)
                self.cash_backtosum_button = ttk.Button(self.method_window_cash, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
                self.cash_backtosum_button.place(x=316, y=110)
                
            self.canvas.pack_forget()
            self.bar.pack_forget()
            self.method_window_main.place(x=0,y=0)
            self.selectpay_head = tkinter.Label(self.method_window_main, text="Select Payment Method", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.selectpay_head.place(x=310, y=0)
            self.credit_button = ttk.Button(self.method_window_main, command=card, text="Credit/Debit Card", style="TButton", width=30)
            self.credit_button.place(x=316, y=40)
            self.bank_button = ttk.Button(self.method_window_main, command=bank, text="Bank Check", style="TButton", width=30)
            self.bank_button.place(x=316, y=70)
            self.cash_button = ttk.Button(self.method_window_main, command=cash, text="Cash on Delivary", style="TButton", width=30)
            self.cash_button.place(x=316, y=100)
            self.backtosum_button = ttk.Button(self.method_window_main, command=backtosum, text="Unsave and Back to Summary", style="TButton", width=30)
            self.backtosum_button.place(x=316, y=130)
            self.savecheck = tkinter.IntVar(value = 0)
            

        def checkout():
            if self.ship_name_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Full Name is empty"))
            elif self.ship_street_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: Street is empty or invalid input"))
            elif self.ship_city_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: City is empty or invalid input"))
            elif self.ship_state_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: State is empty or invalid input"))
            elif self.ship_country_entry.get() == "":
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: Country is empty or invalid input"))
            elif self.ship_zip_entry.get() == "" or is_invalid(self.ship_zip_entry.get()) or len(self.ship_zip_entry.get())<5:
                messagebox.showwarning(title = "ERROR", message = ("Shipping Address: Zip Code is empty or invalid input"))
            elif self.payinfo == [] and self.method != "Cash (on Delivery)":
                messagebox.showwarning(title = "ERROR", message = ("Payment Method is not selected"))
            else:
                maxorderid = len(self.cursor.execute('SELECT * FROM orders').fetchall())
                
                f = open("orderconfirmation_" + self.user_id + "_" + str(maxorderid) +".txt", "w")
                f.write("Order Confirmation\n==================================================================="
                        +"\nOrdered Books:\n===================================================================")
                for i in range(0, len(self.ordersummary)):
                    book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [self.ordersummary[i][0],]).fetchone()
                    f.write("\nTitle: " + str(book[1]) + "\nAuthor: " + str(book[2]) + "\nPublisher: " + str(book[3]) + "\nPrice: " + str(book[4]) + "\nQty: " + str(self.ordersummary[i][1]))
                    f.write("\n===================================================================")
                    self.cursor.execute('UPDATE books SET available=?, sold=? WHERE book_id=?', [(int(book[5]) - self.ordersummary[i][1]), (int(book[6]) + self.ordersummary[i][1]), self.ordersummary[i][0]])
                    
                f.write("\nCustomer Information:\n===================================================================")
                f.write("\nFull Name: " + str(self.ship_name_entry.get()) +
                        "\nShipping Address:" +
                        "\n Street: " + str(self.ship_street_entry.get()) +
                        "\n City: " + str(self.ship_city_entry.get()) +
                        "\n State: " + str(self.ship_state_entry.get()) +
                        "\n Country: " + str(self.ship_country_entry.get()) +
                        "\n Zip: " + str(self.ship_zip_entry.get()))
                f.write("\n===================================================================")
                f.write("\nPayment Information:\n===================================================================")
                f.write("\nPayment Method: " + str(self.method))
                if self.method == "Credit/Debit Card":
                    f.write("\nName on Card: " + str(self.payinfo[1]) +
                            "\nCard Number: " + str(self.payinfo[2]) +
                            "\nCard Exp: " + str(self.payinfo[3]) + "/" + str(self.payinfo[4]) +
                            "\nBilling Address:" +
                            "\n Street: " + str(self.payinfo[5]) +
                            "\n City: " + str(self.payinfo[6]) +
                            "\n State: " + str(self.payinfo[7]) +
                            "\n Country: " + str(self.payinfo[8]) +
                            "\n Zip: " + str(self.payinfo[9]) +
                            "\n Phone: " + str(self.payinfo[10]))
                    self.cursor.execute('SELECT * FROM cards WHERE user_id=?', [self.user_id,])
                    exist = len(self.cursor.fetchall())
                    if exist == 0:
                        if self.savecheck.get() == 1:
                            self.cursor.execute('INSERT into cards values (?,?,?,?,?,?,?,?,?,?,?)', self.payinfo)
                            db.commit()
                    else:
                        if self.savecheck.get() == 1:
                            pinfoforupdate = self.payinfo[1:11]+[self.payinfo[0]]
                            self.cursor.execute('UPDATE cards SET name=?, cardnumber=?, exp_month=?, exp_year=?,\
                                                                  bill_street=?, bill_city=?, bill_state=?, bill_country=?,\
                                                                  bill_zip=?, bill_phone=?\
                                WHERE user_id=?', pinfoforupdate)
                            db.commit()
                        else:
                            self.cursor.execute('DELETE cards WHERE user_id=?', self.user_id)
                            db.commit()
                            
                elif self.method == "Bank Check":
                    f.write("\nName: " + str(self.payinfo[1]) +
                            "\nBank Type: " + str(self.payinfo[2]) +
                            "\nRouting Number: " + str(self.payinfo[3]) +
                            "\nAccount Number: " + str(self.payinfo[4]))
                    self.cursor.execute('SELECT * FROM checks WHERE user_id=?', [self.user_id,])
                    exist = len(self.cursor.fetchall())
                    if exist == 0:
                        if self.savecheck.get() == 2:
                            self.cursor.execute('INSERT into checks values (?,?,?,?,?)', self.payinfo)
                            db.commit()
                    else:
                        if self.savecheck.get() == 2:
                            pinfoforupdate = self.payinfo[1:5]+[self.payinfo[0]]
                            self.cursor.execute('UPDATE checks SET name=?, acctype=?, routing=?, bankacc=? WHERE user_id=?', pinfoforupdate)
                            db.commit()
                        else:
                            self.cursor.execute('DELETE checks WHERE user_id=?', self.user_id)
                            db.commit()
                else:
                    f.write("\nYou must pay when you receive the box.")

                self.cursor.execute('UPDATE accounts SET saved_payment=? WHERE user_id=?', [self.savecheck.get(), self.user_id])
                db.commit()
                

                orderqty = ""
                for x in range(0, len(self.orderbooks)):
                    if x == len(self.orderbooks)-1:
                        orderqty = orderqty + str(self.orderbooks[x])
                    else:
                        orderqty = orderqty + str(self.orderbooks[x])+":"
                    
                total = (round(self.subtotal, 2)+round(self.subtotal * 0.0625))
                
                shipadd =  (str(self.ship_name_entry.get()) + ":" + str(self.ship_street_entry.get()) + ":" + 
                           str(self.ship_city_entry.get()) + ":" + str(self.ship_state_entry.get()) + ":" + 
                           str(self.ship_country_entry.get()) + ":" + str(self.ship_zip_entry.get()))
                paymet = self.method
                for y in range(0, len(self.payinfo)):
                    paymet = paymet + ":" + str(self.payinfo[y])
                
                row = [str(maxorderid), self.user_id, orderqty, total, shipadd, paymet]
                
                self.cursor.execute('INSERT into orders values (?,?,?,?,?,?)', row)
                db.commit()
                    
                f.close()
                messagebox.showinfo(title="Thank You", message="You Purchase has been Completed!\nOrder Confirmation is saved as txt file on your file.\nThank You!")

                self.cursor.close()
                self.selectbook_window.destroy()
                storemainGUI(self.user_id)
            

        def viewsummary():
            self.bookcatalogue.destroy()
            self.selectbook_window_mid.place_forget()
            self.selectbook_window_bot.place_forget()
            self.canvas.config(height = 180)
            
            self.summary_head = tkinter.Label(self.purchase_window_top, text="Order Summary", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.summary_head.place(x=340, y=0)
            self.bkcatalogue_summary = tkinter.Frame(self.canvas,height = 180, width = w, bg = bg_label)
            self.canvas.create_window((0,0), window=self.bkcatalogue_summary, anchor=tkinter.NW, width=self.canvas.cget('width'))

            title_head = tkinter.Label(self.bkcatalogue_summary, text= "Title", font=font_small, fg=fc_label, bg=bg_label)
            title_head.grid(row = 0, column = 1)
            author_head = tkinter.Label(self.bkcatalogue_summary, text= "Author", font=font_small, fg=fc_label, bg=bg_label)
            author_head.grid(row = 0, column = 2)
            publisher_head = tkinter.Label(self.bkcatalogue_summary, text= "Publisher", font=font_small, fg=fc_label, bg=bg_label)
            publisher_head.grid(row = 0, column = 3)
            price_head = tkinter.Label(self.bkcatalogue_summary, text= "Price", font=font_small, fg=fc_label, bg=bg_label)
            price_head.grid(row = 0, column = 4)
            qty_head = tkinter.Label(self.bkcatalogue_summary, text= "Qty", font=font_small, fg=fc_label, bg=bg_label)
            qty_head.grid(row = 0, column = 5)
            self.ordersummary = []
            
            for i in range(0, len(self.orderbooks)):
                bid = int(self.orderbooks[i])
                if bid != 0:
                    self.ordersummary.append([i, bid])
                    book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [i,]).fetchone()
                    title = tkinter.Label(self.bkcatalogue_summary, text= str(book[1]), font=font_small, fg=fc_label, bg=bg_label)
                    author = tkinter.Label(self.bkcatalogue_summary, text= str(book[2]), font=font_small, fg=fc_label, bg=bg_label)
                    publisher = tkinter.Label(self.bkcatalogue_summary, text= str(book[3]), font=font_small, fg=fc_label, bg=bg_label)
                    price = tkinter.Label(self.bkcatalogue_summary, text= ("$" + str(book[4])), font=font_small, fg=fc_label, bg=bg_label)
                    qty = tkinter.Label(self.bkcatalogue_summary, text= str(self.orderbooks[i]), font=font_small, fg=fc_label, bg=bg_label)
                    title.grid(row = len(self.ordersummary) + 1, column = 1, sticky = tkinter.W)
                    author.grid(row = len(self.ordersummary) + 1, column = 2, sticky = tkinter.W)
                    publisher.grid(row = len(self.ordersummary) + 1, column = 3, sticky = tkinter.W)
                    price.grid(row = len(self.ordersummary) + 1, column = 4, sticky = tkinter.W)
                    qty.grid(row = len(self.ordersummary) + 1, column = 5)
            self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 35)

            self.total_head_summary = tkinter.Label(self.purchase_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(round(self.subtotal, 2))),
                                            font=font_normal, fg=fc_label, bg=bg_label)
            self.total_head_summary.place(x=300, y=10)
            self.backtocatalogue_button = ttk.Button(self.purchase_window_bot, command=backtoCatalogue, text="Back to Catalogue", style="TButton", width=20)
            self.backtocatalogue_button.place(x=650, y=4)

            self.ship_head = tkinter.Label(self.purchase_window_bot, text="Shipping Address:", font=font_small_bold, fg=fc_label, bg=bg_label)
            self.ship_name_label = tkinter.Label(self.purchase_window_bot, text="Full Name:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_name_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_street_label = tkinter.Label(self.purchase_window_bot, text="Street:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_street_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_city_label = tkinter.Label(self.purchase_window_bot, text="City:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_city_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_state_label = tkinter.Label(self.purchase_window_bot, text="State:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_state_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_country_label = tkinter.Label(self.purchase_window_bot, text="Country:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_country_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_zip_label = tkinter.Label(self.purchase_window_bot, text="Zipcode:", font=font_small, fg=fc_label, bg=bg_label)
            self.ship_zip_entry = tkinter.Entry(self.purchase_window_bot, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=35)
            self.ship_head.place(x=20, y=70)
            self.ship_name_label.place(x=20, y=50)
            self.ship_name_entry.place(x=86, y=51)
            self.ship_street_label.place(x=20, y=90)
            self.ship_street_entry.place(x=75, y=91)
            self.ship_city_label.place(x=20, y=110)
            self.ship_city_entry.place(x=75, y=111)
            self.ship_state_label.place(x=20, y=130)
            self.ship_state_entry.place(x=75, y=131)
            self.ship_country_label.place(x=20, y=150)
            self.ship_country_entry.place(x=75, y=151)
            self.ship_zip_label.place(x=20, y=170)
            self.ship_zip_entry.place(x=75, y=171)

            self.subandtax = tkinter.Label(self.purchase_window_bot, text=("Subtotal: $" + str(round(self.subtotal, 2)) +
                                                                           "\nTax: $" + str(round(self.subtotal * 0.0625))), font=font_normal, fg=fc_label, bg=bg_label)
            self.taxtotal = tkinter.Label(self.purchase_window_bot, text=("    Total: $" + str(round(self.subtotal, 2)+round(self.subtotal * 0.0625))), font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.subandtax.place(x=500, y=70)
            self.taxtotal.place(x=500, y=130)

            self.pay_head = tkinter.Label(self.purchase_window_bot, text="Payment Method:", font=font_small_bold, fg=fc_label, bg=bg_label)
            self.pay_head.place(x=20, y=210)
            self.pay_method = tkinter.Label(self.purchase_window_bot, text=self.method, font=font_small, fg=fc_label, bg=bg_label)
            self.pay_method.place(x=135, y=210)
            self.pay_select_button = ttk.Button(self.purchase_window_bot, command=selectpayment, text="Select Payment Method", style="TButton", width=20)
            self.pay_select_button.place(x=40, y=235)

            self.confirm_button = ttk.Button(self.purchase_window_bot, command=checkout, text="Place Your Order", style="font_normal.TButton", width=20)
            self.confirm_button.place(x=500, y=200)
            self.pur_cancel_button = ttk.Button(self.purchase_window_bot, command=cancel, text="Cancel", style="TButton", width=15)
            self.pur_cancel_button.place(x=555, y=240)

            self.payinfo = []           
            
            self.purchase_window_top.place(x=0,y=0)
            self.purchase_window_bot.place(x=0,y=215)
            
            

        self.filterbooks_button = ttk.Button(self.selectbook_window_mid, command=filterbooks, text="Filter the Book Catalogue", style="TButton", width=30)
        self.filterbooks_button.place(x=300.5, y=50)
        self.filterreset_button = ttk.Button(self.selectbook_window_mid, command=filterreset, text="Filter Reset", style="TButton", width=15)
        self.filterreset_button.place(x=528, y=25)
        self.bookcatalogue_label = tkinter.Label(self.selectbook_window_mid, text="Book Catalogue", font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.bookcatalogue_label.place(x=340, y=90)
        self.title_label = tkinter.Label(self.selectbook_window_mid, text="Title=", font=font_small, fg=fc_label, bg=bg_label)
        self.title_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
        self.author_label = tkinter.Label(self.selectbook_window_mid, text="Author=", font=font_small, fg=fc_label, bg=bg_label)
        self.author_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
        self.publisher_label = tkinter.Label(self.selectbook_window_mid, text="Publisher=", font=font_small, fg=fc_label, bg=bg_label)
        self.publisher_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=30)
        self.price_label = tkinter.Label(self.selectbook_window_mid, text="Price=", font=font_small, fg=fc_label, bg=bg_label)
        self.price_to = tkinter.Label(self.selectbook_window_mid, text="=<=", font=font_small, fg=fc_label, bg=bg_label)
        self.price_min_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)
        self.price_max_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)
        self.available_label = tkinter.Label(self.selectbook_window_mid, text="Available=", font=font_small, fg=fc_label, bg=bg_label)
        self.available_to = tkinter.Label(self.selectbook_window_mid, text="=<=", font=font_small, fg=fc_label, bg=bg_label)
        self.available_min_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)
        self.available_max_entry = tkinter.Entry(self.selectbook_window_mid, bd=1, font=font_small, fg=fc_entry, bg=bg_entry, width=10)

        #一文字 = x=7, y=22 （おおよそ）entry 219;1=7.3
        self.title_label.place(x=5, y=0)
        self.title_entry.place(x=41, y=0)
        self.author_label.place(x=260, y=0)
        self.author_entry.place(x=309, y=0)
        self.publisher_label.place(x=528, y=0)
        self.publisher_entry.place(x=593, y=0)
        self.price_label.place(x=5, y=25)
        self.price_to.place(x=120, y=25)
        self.price_min_entry.insert(0, int(0))
        self.price_min_entry.place(x=46, y=25)
        self.price_max_entry.insert(0, maxprice)
        self.price_max_entry.place(x=149, y=25)
        self.available_label.place(x=260, y=25)
        self.available_min_entry.insert(0, 0)
        self.available_min_entry.place(x=322, y=25)
        self.available_to.place(x=396, y=25)
        self.available_max_entry.insert(0, maxavailable)
        self.available_max_entry.place(x=425, y=25)

        self.total_head = tkinter.Label(self.selectbook_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(self.subtotal)), font=font_normal_bold, fg=fc_label, bg=bg_label)
        self.total_head.place(x=270, y=10)
        self.vieworder_button = ttk.Button(self.selectbook_window_bot, command=viewsummary, text="Proceed to Checkout", style="font_normal.TButton", width=20)
        self.vieworder_button.place(x=310, y=45)
        self.cartreset_button = ttk.Button(self.selectbook_window_bot, command=cartreset, text="Reset Cart", style="TButton", width=20)
        self.cartreset_button.place(x=650, y=4)
        self.sel_cancel_button = ttk.Button(self.selectbook_window_bot, command=cancel, text="Cancel", style="TButton", width=15)
        self.sel_cancel_button.place(x=365, y=90)

        self.selectbook_window_mid.place(x = 0, y = 0)
        self.selectbook_window_bot.place(x = 0, y = 375)

        #style - appearance of a widget class.
        #the style name of a ttk widget starts with the letter 'T' followed by the widget name - eg, TLabel and TButton
        self.style = ttk.Style()
        self.style.configure("TButton", font=font_small, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        self.style.configure("font_normal.TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)

        self.selectbook_window.mainloop()

#UserInfoGUI: set the userinfo window's appearance and actions
class UserInfoGUI():
    def __init__(self, user_id):
        self.cursor = db.cursor()
        self.user_id = user_id

    #Set the appearance
        self.userinfo_window = tkinter.Tk()
        #Title of the application
        self.userinfo_window.title("Update User Info")
        #Geometry string is a standard way of describing the size and location of the window
        # Set the size of the window (x and  y position of the root window)
        self.userinfo_window.geometry(normal_geo)
        self.userinfo_window.config(bg=bg_normal) #Background color

    #Set the actions
        def edituserinfo():
            row = [self.pass_entry.get(), self.fname_entry.get(), self.lname_entry.get(), self.email_entry.get(), self.user_id]
            self.cursor.execute('UPDATE accounts SET password=?, fname=?, lname=?, email=? WHERE user_id=?', row)
            db.commit()
            messagebox.showinfo(title="Save", message= ("Account infomation is updated!----- \nUser ID: "+ str(self.user_id)
                                                           + "\nPassword: " + str(self.pass_entry.get())
                                                           + "\nFirstname: " + str(self.fname_entry.get())
                                                           + "\nLastname: " + str(self.lname_entry.get())
                                                           + "\nEmail: " + str(self.email_entry.get())))
            self.cursor.close()
            self.userinfo_window.destroy()
            storemainGUI(self.user_id)
            
        def cancel():
            self.cursor.close()
            self.userinfo_window.destroy()
            storemainGUI(self.user_id)

    #Set the detail appearance    
        self.userinfo_head = tkinter.Label(self.userinfo_window, text="User Info Update", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a label for Password
        self.pass_label = tkinter.Label(self.userinfo_window, text="Password:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for Password
        self.pass_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating a label for First Name
        self.fname_label = tkinter.Label(self.userinfo_window, text="First Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for First Name
        self.fname_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating a label for Last Name
        self.lname_label = tkinter.Label(self.userinfo_window, text="Last Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for Last Name
        self.lname_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating a label for Email
        self.email_label = tkinter.Label(self.userinfo_window, text="Email:", font=font_normal_bold, fg=fc_label, bg=bg_label)
        # Creating a text entry box for Email
        self.email_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
        # Creating buttons
        self.save_button = ttk.Button(self.userinfo_window, command = edituserinfo, text = "Update Information", style="TButton", width=20)
        self.cancel_button = ttk.Button(self.userinfo_window, command=cancel, text="Cancel", style="TButton", width=20)

        self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.user_id,])

        # Position the buttons
        self.userdata = self.cursor.fetchone()
                    
        self.pass_entry.insert(0, self.userdata[1])
        self.fname_entry.insert(0, self.userdata[2])
        self.lname_entry.insert(0, self.userdata[3])
        self.email_entry.insert(0, self.userdata[4])

        self.userinfo_head.place(x=180, y=10)
        
        self.pass_label.place(x=5, y=60)
        self.fname_label.place(x=5, y=90)
        self.lname_label.place(x=5, y=120)
        self.email_label.place(x=5, y=150)
            
        self.pass_entry.place(x=200, y=60)
        self.fname_entry.place(x=200, y=90)
        self.lname_entry.place(x=200, y=120)
        self.email_entry.place(x=200, y=150)

        self.save_button.place(x=150, y=190)
        self.cancel_button.place(x=150, y=225)

        self.style = ttk.Style()
        self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        
        #Loop the window
        self.userinfo_window.mainloop()
        

#adminGUI: set the admin window's appearance and actions
class adminGUI():
    def __init__(self):
        self.cursor = db.cursor()
        self.admin_window = tkinter.Tk()

    #Set the appearance
        #Title of the application
        self.admin_window.title("Admin Main")
        #Geometry string is a standard way of describing the size and location of the window
        # Set the size of the window (x and  y position of the root window)
        self.admin_window.geometry(normal_geo)
        self.admin_window.config(bg=bg_normal) #Background color

    #Set the actions
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
            loginGUI()

        #Creating buttons
        self.adminhead = tkinter.Label(self.admin_window, text="Admin Panel", font=font_normal, fg=fc_label, bg=bg_label)
        self.adminhead.place(x=203, y=0)
        self.adduser_button = ttk.Button(self.admin_window, command=adduser, text="Save New User Account", style="TButton", width=20)
        self.adduser_button.place(x=150, y=35)
        self.edituser_button = ttk.Button(self.admin_window, command=edituser, text="Edit User Account", style="TButton", width=20)
        self.edituser_button.place(x=150, y=75)
        self.addbook_button = ttk.Button(self.admin_window, command=addbook, text="Save New Book", style="TButton", width=20)
        self.addbook_button.place(x=150, y=115)
        self.editbook_button = ttk.Button(self.admin_window, command=editbook, text="Edit Book", style="TButton", width=20)
        self.editbook_button.place(x=150, y=155)
        self.vieworder_button = ttk.Button(self.admin_window, command=vieworder, text="View Orders", style="TButton", width=20)
        self.vieworder_button.place(x=150, y=195)
        self.Logout_button = ttk.Button(self.admin_window, command=logout, text="Logout", style="logout.TButton", width=20)
        self.Logout_button.place(x=150, y=235)
        
        self.style = ttk.Style()
        self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        self.style.configure("logout.TButton", font=font_normal, foreground="#C32148", background=bg_button, activeforeground=bg_entry, activebackground=fg_button)

        #Loop the window
        self.admin_window.mainloop()

#UserManageGUI: set the user manage window (for admin)'s appearance and actions
class UserManageGUI():
    def __init__(self, flag):
        self.cursor = db.cursor()

    #Set the actions
        def adduser():
            self.acc_window.geometry(normal_geo)
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

        def getuserinfo(userid):
            self.acc_window.geometry(normal_geo)
            self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [userid,])

            self.userdata = self.cursor.fetchone()
                    
            self.pass_entry.insert(0, self.userdata[1])
            self.fname_entry.insert(0, self.userdata[2])
            self.lname_entry.insert(0, self.userdata[3])
            self.email_entry.insert(0, self.userdata[4])
            self.saved_payment_entry.insert(0, self.userdata[5])
            self.user_id = userid
            placelines(edituser,"Update User Info")

        def placelines(com,tex):

            self.save_button = ttk.Button(self.acc_window, command = com, text = tex, style="TButton", width=20)
            self.method_label = tkinter.Label(self.acc_window, text="1: Card/2: Check/3: Cash/0: None", font=font_normal_bold, fg=fc_label, bg=bg_normal)
            
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
                
                self.delete_button = ttk.Button(self.acc_window, command = deleteuser, text = "Delete the User", style="TButton", width=20)
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

        def convertpayment(num):
            #saved_payment:
            #0: no data
            #1: card
            #2: check
            #3: cash(on delivery)

            if num == 1:
                return "Card"
            elif num == 2:
                return "Check"
            elif num == 3:
                return "Cash (on delivery)"
            else:
                return "None"

        def cancel():
            self.acc_window.destroy()
            adminGUI()

        def back():
            self.acc_window.destroy()
            setlist()
            
        def setlist():
        #Set the appearance
            self.acc_window = tkinter.Tk()
            #Title of the application
            self.acc_window.title("Manage Accounts")

            self.acc_window.geometry(list_geo)
            self.acc_window.config(bg=bg_normal) #Background color
            
            # Creating a label for User ID
            self.userid_label = tkinter.Label(self.acc_window, text="User ID:", font=font_normal_bold, fg=fc_label, bg=bg_label)

            # Creating a text entry box for User ID
            self.userid_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label for Password
            self.pass_label = tkinter.Label(self.acc_window, text="Password:", font=font_normal_bold, fg=fc_label, bg=bg_label)

            # Creating a text entry box for Password
            self.pass_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
            
            # Creating a label for First Name
            self.fname_label = tkinter.Label(self.acc_window, text="First Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)

            # Creating a text entry box for First Name
            self.fname_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label for Last Name
            self.lname_label = tkinter.Label(self.acc_window, text="Last Name:", font=font_normal_bold, fg=fc_label, bg=bg_label)

            # Creating a text entry box for Last Name
            self.lname_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
                
            # Creating a label for Email
            self.email_label = tkinter.Label(self.acc_window, text="Email:", font=font_normal_bold, fg=fc_label, bg=bg_label)
                
            # Creating a text entry box for Email
            self.email_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

            # Creating a label for Payment Method
            self.saved_payment_label = tkinter.Label(self.acc_window, text="Payment method:", font=font_normal_bold, fg=fc_label, bg=bg_label)
                
            # Creating a text entry box for Payment Method
            self.saved_payment_entry = tkinter.Entry(self.acc_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)
            
            # Creating a cancel button
            self.cancel_button = ttk.Button(self.acc_window, command=cancel, text="Cancel", style="TButton", width=20)
            self.back_button = ttk.Button(self.acc_window, command=back, text="Back", style="TButton", width=20)
            
            # Creating the frame for list view (as same as book list in BuyBookGUI)     
            if flag == True: #edit user

                canvas = tkinter.Canvas(self.acc_window, bg =bg_normal, height = 600, width= 1000)

               # Scrollbar を生成して配置
                bar = tkinter.Scrollbar(self.acc_window, orient=tkinter.VERTICAL)
                bar.pack(side=tkinter.RIGHT, ipady = 600)
                bar.config(command=canvas.yview)

                canvas.config(yscrollcommand=bar.set) #スクロール範囲

                # Frame Widgetを 生成
                frame = tkinter.Frame(canvas)

                # Frame Widgetを Canvas Widget上に配置
                canvas.create_window((0,0), window=frame, anchor=tkinter.NW, width=canvas.cget('width'))

                def set_userid():
                    getuserinfo(ids[var.get()])
                    canvas.destroy()
                    self.chooseone.destroy()
                    self.cancel_button.destroy()

                # 複数の Button Widget 生成し、Frame上に配置
                self.cursor.execute('SELECT * FROM accounts')
                accs = self.cursor.fetchall()
                canvas.config(scrollregion=(0,0,50,len(accs)*55))
                var = tkinter.IntVar()
                ids =[]
                ind = 0
                for bk in accs:
                    ids.append(bk[0])
                    txt = ("UserID: %s"%str(bk[0]) + "/ Password: %s"%str(bk[1]) + "/ Firstname: %s"%str(bk[2]) + "/ Lastname: %s"%str(bk[3]) + "/ Email: %s"%str(bk[4]) + "/ Payment method: %s"%str(bk[5]))
                    bt = tkinter.Radiobutton(frame, text=txt, bg =bg_normal, variable = var, value = ind, command=set_userid)
                    ind = ind + 1
                    bt.pack(fill=tkinter.X)

                canvas.pack(side=tkinter.TOP, pady= 50)

                self.chooseone = tkinter.Label(self.acc_window, text = "Choose an account for edit", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.chooseone.place(x=554, y=10)
                self.cancel_button.lift()
                self.cancel_button.place(x=550, y=670)

            else: #add new user
                placelines(adduser, "Save New User")
                
            self.style = ttk.Style()
            self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)

            #Loop the window
            self.acc_window.mainloop()

        setlist()
        

#BookManageGUI: set the book manage window (for admin)'s appearance and actions
class BookManageGUI():
    def __init__(self, flag):
        self.cursor = db.cursor()

    #Set the actions
        def addbook():
            self.book_window.geometry(normal_geo)
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
            adminGUI()

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

        def getbookinfo(bookid):
            self.book_window.geometry(normal_geo)
            self.cursor.execute('SELECT * FROM books WHERE book_id=?', [bookid, ])

            self.bookdata = self.cursor.fetchone()
                    
            self.title_entry.insert(0, self.bookdata[1])
            self.author_entry.insert(0, self.bookdata[2])
            self.publisher_entry.insert(0, self.bookdata[3])
            self.price_entry.insert(0, self.bookdata[4])
            self.available_entry.delete(0)
            self.available_entry.insert(0, self.bookdata[5])
            self.bookid = bookid
            placelines(editbook,"Update Book Info")

        def placelines(com,tex):

            self.save_button = ttk.Button(self.book_window, command = com, text = tex, style="TButton", width=20)
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
                self.delete_button = ttk.Button(self.book_window, command = deletebook, text = "Delete the Book", style="TButton", width=20)
                self.delete_button.place(x=260, y=190)
                self.back_button.place(x=150, y=230)

            else:
                self.cancel_button.place(x=260, y=190)

        def cancel():
            self.book_window.destroy()
            adminGUI()

        def back():
            self.book_window.destroy()
            setlist()
            
        def setlist(): 
            self.book_window = tkinter.Tk()
            #Title of the application
            self.book_window.title("Manage Book Catalogue")

            self.book_window.geometry(list_geo)
            self.book_window.config(bg=bg_normal) #Background color

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
            
            #Creating buttons
            self.cancel_button = ttk.Button(self.book_window, command=cancel, text="Cancel", style="TButton", width=20)
            self.back_button = ttk.Button(self.book_window, command=back, text="Back", style="TButton", width=20)

            # Creating the frame for list view (as same as book list in BuyBookGUI)
            if flag == True: #edit book

                canvas = tkinter.Canvas(self.book_window, bg =bg_normal, height = 600, width= 1000)

               # Scrollbar を生成して配置
                bar = tkinter.Scrollbar(self.book_window, orient=tkinter.VERTICAL)
                bar.pack(side=tkinter.RIGHT, ipady = 600)
                bar.config(command=canvas.yview)

                canvas.config(yscrollcommand=bar.set)#スクロール範囲

                # Frame Widgetを 生成
                frame = tkinter.Frame(canvas)

                # Frame Widgetを Canvas Widget上に配置
                canvas.create_window((0,0), window=frame, anchor=tkinter.NW, width=canvas.cget('width'))

                def set_bookid():
                    getbookinfo(ids[var.get()])
                    canvas.destroy()
                    self.chooseone.destroy()
                    self.cancel_button.destroy()

                # 複数の Button Widget 生成し、Frame上に配置
                self.cursor.execute('SELECT * FROM books')
                bks = self.cursor.fetchall()
                canvas.config(scrollregion=(0,0,canvas.cget('width'),len(bks)*25))
                var = tkinter.IntVar()
                ids =[]
                ind = 0
                for bk in bks:
                    ids.append(bk[0])
                    txt = ("BookID: %s"%str(bk[0]) + "/ Title: %s"%str(bk[1]) + "/ Author: %s"%str(bk[2]) + "/ Publisher: %s"%str(bk[3]) + "/ Price: %s"%str(bk[4]) + "/ Availability: %s"%str(bk[5]))
                    bt = tkinter.Radiobutton(frame, text=txt, bg =bg_normal, variable = var, value = ind, command=set_bookid)
                    ind = ind + 1
                    bt.pack(fill=tkinter.X)

                canvas.pack(side=tkinter.TOP, pady= 50)

                self.chooseone = tkinter.Label(self.book_window, text = "Choose a book for edit", font=font_normal_bold, fg=fc_label, bg=bg_label)
                self.chooseone.place(x=554, y=10)
                self.cancel_button.lift()
                self.cancel_button.place(x=550, y=670)

            else: #add new book
                placelines(addbook, "Save New Book")
                
            self.style = ttk.Style()
            self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)

            #Loop the window
            self.book_window.mainloop()

        setlist()

class ViewOrderGUI():
    def __init__(self): #storemainGUI()に呼び出されるGUIは全部user_idを参照する
        self.cursor = db.cursor()

    #Set the appearance
        self.vieworder_window = tkinter.Tk() #bookcatalogue一覧から選ぶ -> 選択画面がメインウィンドウのGUI(user_id)
        self.vieworder_window.title("View Order")
        self.vieworder_window.geometry("820x500")
        h = 500
        w = 820
        self.bgcolor = bg_normal
        self.bgcolor2 = "#AFDCEC"
        self.vieworder_window.config(bg = self.bgcolor) 

        self.vieworder_window_top = tkinter.Frame(height = 40, width = w, bg = self.bgcolor) #カタログのフィルタリング →第二フレーム
        self.vieworder_window_bot = tkinter.Frame(height = 40, width = w, bg = self.bgcolor) #合計金額の計算　→　第三フレーム
        self.vieworder_detail_bot = tkinter.Frame(height=40, width = 820, bg = self.bgcolor) #支払い方法の入力　→　オーバーｒｙその③

        # Creating the frame for list view (as same as book list in BuyBookGUI)
        
        #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）

        # Scrollbar を生成して配置
        self.canvas = tkinter.Canvas(self.vieworder_window, bg =self.bgcolor, height = 460, width= w)
        self.bar = tkinter.Scrollbar(self.vieworder_window, orient=tkinter.VERTICAL)
        
        self.bar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.bar.set)
        
    #Set the actions
        def cancel():
            self.cursor.close()
            self.vieworder_window.destroy()
            adminGUI()
        
        def createorderslist(conn):
            def viewdetail():
                def backtolist():
                    self.vieworder_detail.destroy()
                    self.vieworder_detail_bot.place_forget()
                    
                    createorderslist(self.cursor.execute('SELECT * FROM orders'))

                self.orderlist.destroy()
                self.vieworder_detail = tkinter.Frame(self.canvas, height=460, width = 820, bg = bg_label)
                self.canvas.create_window((0,0), window=self.vieworder_detail, anchor=tkinter.NW, width=self.canvas.cget('width'))
                self.canvas.config(height = 460, width = 820)

                txt = ("Order Detail\n==================================================================="
                            +"\nOrdered Books:\n===================================================================")
                order = self.cursor.execute('SELECT * FROM orders WHERE order_id =?', [self.var.get(),]).fetchone()
                booklist = [int(x) for x in order[2].split(":")]
                for i in range(0, len(booklist)):
                    if booklist[i] != 0:
                        book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [i,]).fetchone()
                        txt = txt + ("\nTitle: " + str(book[1]) + "\nAuthor: " + str(book[2]) + "\nPublisher: " + str(book[3])
                                     + "\nPrice: " + str(book[4]) + "\nQty: " + str(booklist[i]))
                        txt = txt + ("\n===================================================================")
                         
                txt = txt + ("\nCustomer Information:\n===================================================================")
                order = self.cursor.execute('SELECT * FROM orders WHERE order_id =?', [self.var.get(),]).fetchone()
                shipinfo = order[4].split(":")
                txt = txt + ("\nFull Name: " + str(shipinfo[0]) +
                            "\nShipping Address:" +
                            "\n Street: " + str(shipinfo[1]) +
                            "\n City: " + str(shipinfo[2]) +
                            "\n State: " + str(shipinfo[3]) +
                            "\n Country: " + str(shipinfo[4]) +
                            "\n Zip: " + str(shipinfo[5]))
                txt = txt + ("\n===================================================================")
                txt = txt + ("\nPayment Information:\n===================================================================")
                order = self.cursor.execute('SELECT * FROM orders WHERE order_id =?', [self.var.get(),]).fetchone()
                payinfo = order[5].split(":")
                txt = txt + ("\nPayment Method: " + str(payinfo[0]))
                if payinfo[0] == "Credit/Debit Card":
                    txt = txt + ("\nName on Card: " + str(payinfo[2]) +
                            "\nCard Number: " + str(payinfo[3]) +
                            "\nCard Exp: " + str(payinfo[4]) + "/" + str(payinfo[5]) +
                            "\nBilling Address:" +
                            "\n Street: " + str(payinfo[6]) +
                            "\n City: " + str(payinfo[7]) +
                            "\n State: " + str(payinfo[8]) +
                            "\n Country: " + str(payinfo[9]) +
                            "\n Zip: " + str(payinfo[10]) +
                            "\n Phone: " + str(payinfo[11]))
                elif payinfo[0] == "Bank Check":
                    txt = txt + ("\nName: " + str(payinfo[2]) +
                            "\nBank Type: " + str(payinfo[3]) +
                            "\nRouting Number: " + str(payinfo[4]) +
                            "\nAccount Number: " + str(payinfo[5]))
                else:
                    txt = txt + ("\nYou must pay when you receive the box.")

                info = tkinter.Label(self.vieworder_detail, text= txt, font=font_small, fg=fc_label, bg=bg_label)
                info.place(x=0,y=0)
                self.canvas.config(scrollregion=(0,0,50,len(booklist)*30))
                self.vieworder_detail.config(height = len(booklist)*30)
                self.bar.pack(side=tkinter.RIGHT,  pady=0, ipady =0, fill =tkinter.Y)
                self.canvas.pack(side=tkinter.TOP, pady=0)

                self.backtolist_button = ttk.Button(self.vieworder_detail_bot, command = backtolist, text = "Back to View Order", style="TButton", width=20)
                self.backtolist_button.place(x=360, y=10)
                self.vieworder_detail_bot.place(x=0,y=460)
            
            self.var = tkinter.IntVar(value = 0)
            self.orderlist = tkinter.Frame(self.canvas,height = 460, width = w, bg = bg_label)
            self.canvas.config(height = 420)
            self.canvas.create_window((0,0), window=self.orderlist, anchor=tkinter.NW, width=self.canvas.cget('width'))
            self.selectedorders = conn.fetchall()
            self.canvas.config(scrollregion=(0,0,50,1000 + len(self.selectedorders)*30)) #スクロール範囲
            oid_head = tkinter.Label(self.orderlist, text= "order ID", font=font_small, fg=fc_label, bg=bg_label)
            oid_head.grid(row = 0, column = 1)
            uid_head = tkinter.Label(self.orderlist, text= "user ID", font=font_small, fg=fc_label, bg=bg_label)
            uid_head.grid(row = 0, column = 2)
            qty_head = tkinter.Label(self.orderlist, text= "Total Qty", font=font_small, fg=fc_label, bg=bg_label)
            qty_head.grid(row = 0, column = 3)
            price_head = tkinter.Label(self.orderlist, text= "Total Price", font=font_small, fg=fc_label, bg=bg_label)
            price_head.grid(row = 0, column = 4)
            method_head = tkinter.Label(self.orderlist, text= "Payment Method", font=font_small, fg=fc_label, bg=bg_label)
            method_head.grid(row = 0, column = 5)
            detail_head = tkinter.Label(self.orderlist, text= "Show Detail", font=font_small, fg=fc_label, bg=bg_label)
            detail_head.grid(row = 0, column = 6)
            
            for order in self.selectedorders:
                print(str(order[0]))
                oid = tkinter.Label(self.orderlist, text= str(order[0]), font=font_small, fg=fc_label, bg=bg_label)
                uid = tkinter.Label(self.orderlist, text= str(order[1]), font=font_small, fg=fc_label, bg=bg_label)
                qty = tkinter.Label(self.orderlist, text= str(sum([int(x) for x in order[2].split(":")])), font=font_small, fg=fc_label, bg=bg_label)
                price = tkinter.Label(self.orderlist, text= ("$" +str(order[3])), font=font_small, fg=fc_label, bg=bg_label)
                method = tkinter.Label(self.orderlist, text= str(order[5].split(":")[0]), font=font_small, fg=fc_label, bg=bg_label)
                print(order[5])
                detail = tkinter.Radiobutton(self.orderlist, variable=self.var, value=int(order[0]), command = viewdetail, fg=fc_label, bg=bg_label)
                detail.deselect()
                oid.grid(row = int(order[0]) + 1, column = 1, sticky = tkinter.W)
                uid.grid(row = int(order[0]) + 1, column = 2, sticky = tkinter.W)
                qty.grid(row = int(order[0]) + 1, column = 3, sticky = tkinter.W)
                price.grid(row = int(order[0]) + 1, column = 4, sticky = tkinter.W)
                method.grid(row = int(order[0]) + 1, column = 5, sticky = tkinter.W)
                detail.grid(row = int(order[0]) + 1, column = 6)

            self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =195, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 35)

            self.vieworder_head = tkinter.Label(self.vieworder_window_top, text= "View Order", font=font_normal_bold, fg=fc_label, bg=bg_label)
            self.vieworder_head.place(x=360, y=0)
            self.vieworder_window_top.place(x=0,y=0)

            self.cancel_button = ttk.Button(self.vieworder_window_bot, command=cancel, text="Cancel", style="TButton", width=15)
            self.cancel_button.place(x=365, y=5)
            self.vieworder_window_bot.place(x=0,y=460)
            
            

        createorderslist(self.cursor.execute('SELECT * FROM orders'))
        

 
loginGUI()
