from re import A
import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
import sqlite3
import os
from variables import *

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
        self.selectbook_window.geometry(multiframe_geo)
        self.selectbook_window.config(bg = bg_normal)

        self.selectbook_window_mid = tkinter.Frame(height = 125, width = multiframe_w, bg = bg_normal) #カタログのフィルタリング →第二フレーム
        self.selectbook_window_bot = tkinter.Frame(height = 175, width = multiframe_w, bg = bg_normal) #合計金額の計算　→　第三フレーム
        self.purchase_window_top = tkinter.Frame(height = 30, width = multiframe_w, bg = bg_normal) #会計　→　オーバーレイフレームその②
        self.purchase_window_bot = tkinter.Frame(height = 300, width = multiframe_w, bg = bg_normal) #会計　→　オーバーレイフレームその②
        self.method_window_main = tkinter.Frame(height = multiframe_h, width = multiframe_w, bg = bg_normal) #支払い方法の入力　→　オーバーｒｙその③
        self.method_window_card = tkinter.Frame(height = 300, width = multiframe_w, bg = bg_method)
        self.method_window_cash = tkinter.Frame(height = 150, width = multiframe_w, bg = bg_method)
        self.method_window_bank = tkinter.Frame(height = 300, width = multiframe_w, bg = bg_method)

        self.canvas = tkinter.Canvas(self.selectbook_window, bg =bg_normal, height = 275, width= multiframe_w) #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）

        # Scrollbar を生成して配置
        self.bar = tkinter.Scrollbar(self.selectbook_window, orient=tkinter.VERTICAL)
        
        self.bar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.bar.set)
        

        # Frame Widgetを 生成
        #frame = tkinter.Frame(canvas,height = 200, width = multiframe_w, bg = bg_label) #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）

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
            from main import StoreMainGUI
            StoreMainGUI(self.user_id)
        

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
                    self.total_head = create_label_frame(self.selectbook_window_bot, ("Subtotal(" + str(self.qtytotal) + " books): $" + str(round(self.subtotal, 2))), 300, 10)
                    self.orderbooks[self.listofbooks[i][0]] = self.numberofbooks[i].get()
                    
            

        # 複数の Button Widget 生成し、Frame上に配置 = スクロールして本を選ぶという動作を成立させる
        
        self.listofbooks = []
        self.priceofbooks = []
        self.numberofbooks = []
        def createbookslist(conn):
            self.listofbooks = []
            self.priceofbooks = []
            self.numberofbooks = []
            self.bookcatalogue = tkinter.Frame(self.canvas,height = 200, width = multiframe_w, bg = bg_label)

            self.canvas.config(height = 275)
            self.canvas.create_window((0,0), window=self.bookcatalogue, anchor=tkinter.NW, width=self.canvas.cget('width'))
            selectedbooks = conn.fetchall()
            self.canvas.config(scrollregion=(0,0,50,len(selectedbooks)*30)) #スクロール範囲
            title_head = create_label_frame_small(self.bookcatalogue, "Title", False)
            author_head = create_label_frame_small(self.bookcatalogue, "Author", False)
            publisher_head = create_label_frame_small(self.bookcatalogue, "Publisher", False)
            price_head = create_label_frame_small(self.bookcatalogue, "Price", False)
            available_head = create_label_frame_small(self.bookcatalogue, "Availablity", False)
            qty_head = create_label_frame_small(self.bookcatalogue, "Qty", False)

            title_head.grid(row = 0, column = 1)
            author_head.grid(row = 0, column = 2)
            publisher_head.grid(row = 0, column = 3)
            price_head.grid(row = 0, column = 4)
            available_head.grid(row = 0, column = 5)
            qty_head.grid(row = 0, column = 6)
            
            for bk in selectedbooks:
                self.listofbooks.append(bk)
                var = tkinter.DoubleVar()
                title = create_label_frame_small(self.bookcatalogue, str(bk[1]), False)
                author = create_label_frame_small(self.bookcatalogue, str(bk[2]), False)
                publisher = create_label_frame_small(self.bookcatalogue, str(bk[3]), False)
                price = create_label_frame_small(self.bookcatalogue, ("$" + str(bk[4])), False)
                available = create_label_frame_small(self.bookcatalogue, str(bk[5]), False)
                unavailable = create_label_frame_small(self.bookcatalogue, "Unavailable", False)
                numofbk = tkinter.Spinbox(self.bookcatalogue, from_=0, to=bk[5], width = 20, command = calctotalprice)
                numofbk.configure(width = 5)
                numofbk.delete(0)
                if self.orderbooks[bk[0]] != 0:
                    numofbk.insert(0, int(self.orderbooks[bk[0]]))
                else:
                    numofbk.insert(0,0)
                self.priceofbooks.append(bk[4])
                self.numberofbooks.append(numofbk)
                grid_ind = len(self.priceofbooks) + 1
                title.grid(row = grid_ind, column = 1, sticky = tkinter.W)
                author.grid(row = grid_ind, column = 2, sticky = tkinter.W)
                publisher.grid(row = grid_ind, column = 3, sticky = tkinter.W)
                price.grid(row = grid_ind, column = 4, sticky = tkinter.W)
                available.grid(row = grid_ind, column = 5)
                if bk[5] != 0:
                    numofbk.grid(row = grid_ind, column=6)
                else:
                    unavailable.grid(row = grid_ind, column=6)

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
            self.bookcatalogue.destroy()
            createbookslist(self.cursor.execute('SELECT * FROM books'))

        def cartreset():
            maxid = self.cursor.execute('SELECT Max(book_id) FROM books').fetchone()[0]
            if maxid != None:
                self.orderbooks = [0]* (maxid + 1)
            else: self.orderbooks = [0]
            self.qtytotal = 0
            self.subtotal = 0
            self.total_head.destroy()
            self.bookcatalogue.destroy()
            self.total_head = create_label_frame(self.selectbook_window_bot, ("Subtotal(" + str(self.qtytotal) + " books): $" + str(self.subtotal)), 300, 10)
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
                self.pay_method = create_label_frame_small(self.purchase_window_bot, self.method, False)
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

                self.card_selectpay_head = create_label_frame(self.method_window_card, "Card Information", 350, 5)

                self.cardinfo_head = create_label_frame_small(self.method_window_card, "Card Detail:", True)
                self.cardname_label = create_label_frame_small(self.method_window_card, "Name on Card:", False)
                self.cardname_entry = create_entry_frame_small(self.method_window_card, width=30)

                self.cardnumber_label = create_label_frame_small(self.method_window_card, "Card Number:", False)
                self.nospace = create_label_frame_small(self.method_window_card, "(no space)", False)
                self.cardnumber_entry = create_entry_frame_small(self.method_window_card, width=30)

                self.cardexp_label = create_label_frame_small(self.method_window_card, "Expire MM/YY:", False)
                self.cardexpmon_entry = create_entry_frame_small(self.method_window_card, width=3)
                self.cardexpto_label = create_label_frame_small(self.method_window_card, "/", False)
                self.cardexpyear_entry = create_entry_frame_small(self.method_window_card, width=3)

                self.cardcvc_label = create_label_frame_small(self.method_window_card, "CVC:", False)
                self.cardcvc_entry = tkinter.Entry(self.method_window_card, bd=1, font=font_small, show = "*", fg=fc_entry, bg=bg_entry, width=5)

                self.cardphone_label = create_label_frame_small(self.method_window_card, "Phone:", False)
                self.cardphone_entry = create_entry_frame_small(self.method_window_card, width=30)

                
                
                
                self.bill_head  = create_label_frame_small(self.method_window_card, "Billing Address:", True)
                self.bill_street_label = create_label_frame_small(self.method_window_card, "Street:", False)
                self.bill_street_entry = create_entry_frame_small(self.method_window_card, width=35)

                self.bill_city_label = create_label_frame_small(self.method_window_card, "City:", False)
                self.bill_city_entry = create_entry_frame_small(self.method_window_card, width=35)

                self.bill_state_label = create_label_frame_small(self.method_window_card, "State:", False)
                self.bill_state_entry = create_entry_frame_small(self.method_window_card, width=35)

                self.bill_country_label = create_label_frame_small(self.method_window_card, "Country:", False)
                self.bill_country_entry = create_entry_frame_small(self.method_window_card, width=35)

                self.bill_zip_label = create_label_frame_small(self.method_window_card, "ZipCode:", False)
                self.bill_zip_entry = create_entry_frame_small(self.method_window_card, width=35)

                self.card_savemethod_button = tkinter.Checkbutton(self.method_window_card, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 1, offvalue = 0, font = font_small, bg = bg_method)
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

                self.savecard_button = create_button_xy(self.method_window_card, "Save Payment Method", savecard, "TButton", 316, 220, 30)
                self.card_backtosum_button = create_button_xy(self.method_window_card, "Unsave and Back to Summary", backtosum, "TButton", 316, 250, 30)
                
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

                self.bank_selectpay_head = create_label_frame(self.method_window_bank, "Bank Information", 350, 5)

                self.bankinfo_head = create_label_frame_small(self.method_window_bank, "Bank Detail:", True)
                self.bankname_label = create_label_frame_small(self.method_window_bank, "Bank Name:", False)
                self.bankname_entry = create_entry_frame_small(self.method_window_bank, width=30)

                self.banktype = tkinter.StringVar(value="None")
                self.banktype_label = create_label_frame_small(self.method_window_bank, "Account Type:", False)
                self.banktype_entry = tkinter.OptionMenu(self.method_window_bank, self.banktype, "Checking", "Saving" )

                self.routing_label = create_label_frame_small(self.method_window_bank, "Routing Number:", False)
                self.routing_entry = create_entry_frame_small(self.method_window_bank, width=30)

                self.bankacc_label = create_label_frame_small(self.method_window_bank, "Account Number:", False)
                self.bankacc_entry = create_entry_frame_small(self.method_window_bank, width=30)

                self.bank_savemethod_button = tkinter.Checkbutton(self.method_window_bank, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 2, offvalue = 0, font = font_small, bg = bg_method)
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

                self.savebank_button = create_button_xy(self.method_window_bank, "Save Payment Method", savebank, "TButton", 316, 220, 30)
                self.bank_backtosum_button = create_button_xy(self.method_window_bank, "Unsave and Back to Summary", backtosum, "TButton", 316, 250, 30)
                
                self.method_window_bank.place(x=0,y=130)

            def cash():
                self.savecheck = tkinter.IntVar(value = 0)
                self.method_window_card.place_forget()
                self.method_window_bank.place_forget()
                self.method_window_cash.place(x=0,y=130)
                self.method = "Cash (on Delivery)"

                self.cash_head = create_label_frame(self.method_window_cash, "You must pay when you receive the box.", 230, 10)

                self.cash_savemethod_button = tkinter.Checkbutton(self.method_window_cash, text = "Save this method for next purchase?",
                                                             variable = self.savecheck, onvalue = 3, offvalue = 0, font = font_small, bg = bg_method)
                self.cash_savemethod_button.deselect()

                pmethod = self.cursor.execute('SELECT saved_payment FROM accounts WHERE user_id=?', [self.user_id,]).fetchone()[0]

                if pmethod == 3:
                    self.cash_savemethod_button.select()
                    
                self.cash_savemethod_button.place(x=305, y=40)

                self.savecash_button = create_button_xy(self.method_window_cash, "Save Payment Method", gotopay, "TButton", 316, 80, 30)
                self.cash_backtosum_button = create_button_xy(self.method_window_cash, "Unsave and Back to Summary", backtosum, "TButton", 316, 110, 30)
                
            self.canvas.pack_forget()
            self.bar.pack_forget()
            self.method_window_main.place(x=0,y=0)
            self.selectpay_head = create_label_frame(self.method_window_main, "Select Payment Method", 310, 0)
            self.credit_button = create_button_xy(self.method_window_main, "Credit/Debit Card", card, "TButton", 316, 40, 30)
            self.bank_button = create_button_xy(self.method_window_main, "Bank Check", bank, "TButton", 316, 70, 30)
            self.cash_button = create_button_xy(self.method_window_main, "Cash on Delivary", cash, "TButton", 316, 100, 30)
            self.backtosum_button = create_button_xy(self.method_window_main, "Unsave and Back to Summary", backtosum, "TButton", 316, 130, 30)

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
                
                try:
                    f = None
                    
                    db.execute("BEGIN TRANSACTION;")
                    
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
                        else:
                            if self.savecheck.get() == 1:
                                pinfoforupdate = self.payinfo[1:11]+[self.payinfo[0]]
                                self.cursor.execute('UPDATE cards SET name=?, cardnumber=?, exp_month=?, exp_year=?,\
                                                                      bill_street=?, bill_city=?, bill_state=?, bill_country=?,\
                                                                      bill_zip=?, bill_phone=?\
                                    WHERE user_id=?', pinfoforupdate)
                            else:
                                self.cursor.execute('DELETE cards WHERE user_id=?', self.user_id)
                            
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
                        else:
                            if self.savecheck.get() == 2:
                                pinfoforupdate = self.payinfo[1:5]+[self.payinfo[0]]
                                self.cursor.execute('UPDATE checks SET name=?, acctype=?, routing=?, bankacc=? WHERE user_id=?', pinfoforupdate)
                            else:
                                self.cursor.execute('DELETE checks WHERE user_id=?', self.user_id)
                    else:
                        f.write("\nYou must pay when you receive the box.")

                    self.cursor.execute('UPDATE accounts SET saved_payment=? WHERE user_id=?', [self.savecheck.get(), self.user_id])
                

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
                    messagebox.showinfo(title="Thank You", message="You Purchase has been Completed!\nOrder Confirmation is saved as txt file on your program's folder.\nThank You!")
                    
                except Exception as e:
                    db.rollback()
                    messagebox.showerror(title="ERROR", message=f"An error occurred during the purchase.\nPurchase isn't completed.\n\nError Details: {e}")

                finally:
                    if f:
                        f.close()
                    self.cursor.close()
                    self.selectbook_window.destroy()
                    from main import StoreMainGUI
                    StoreMainGUI(self.user_id)
            

        def viewsummary():
            self.bookcatalogue.destroy()
            self.selectbook_window_mid.place_forget()
            self.selectbook_window_bot.place_forget()
            self.canvas.config(height = 180)
            
            self.summary_head = create_label_frame(self.purchase_window_top, "Order Summary", 340, 0)
            self.bkcatalogue_summary = tkinter.Frame(self.canvas,height = 180, width = multiframe_w, bg = bg_label)
            self.canvas.create_window((0,0), window=self.bkcatalogue_summary, anchor=tkinter.NW, width=self.canvas.cget('width'))

            title_head = create_label_frame_small(self.bkcatalogue_summary, "Title", False)
            author_head = create_label_frame_small(self.bkcatalogue_summary, "Author", False)
            publisher_head = create_label_frame_small(self.bkcatalogue_summary, "Publisher", False)
            price_head = create_label_frame_small(self.bkcatalogue_summary, "Price", False)
            qty_head = create_label_frame_small(self.bkcatalogue_summary, "Qty", False)

            title_head.grid(row = 0, column = 1)
            author_head.grid(row = 0, column = 2)
            publisher_head.grid(row = 0, column = 3)
            price_head.grid(row = 0, column = 4)
            qty_head.grid(row = 0, column = 5)

            self.ordersummary = []
            
            for i in range(0, len(self.orderbooks)):
                bid = int(self.orderbooks[i])
                if bid != 0:
                    self.ordersummary.append([i, bid])
                    book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [i,]).fetchone()
                    title = create_label_frame_small(self.bkcatalogue_summary, str(book[1]), False)
                    author = create_label_frame_small(self.bkcatalogue_summary, str(book[2]), False)
                    publisher = create_label_frame_small(self.bkcatalogue_summary, str(book[3]), False)
                    price = create_label_frame_small(self.bkcatalogue_summary, str(book[4]), False)
                    qty = create_label_frame_small(self.bkcatalogue_summary, str(self.orderbooks[i]), False)

                    grid_ind = len(self.ordersummary) + 1
                    title.grid(row = grid_ind, column = 1, sticky = tkinter.W)
                    author.grid(row = grid_ind, column = 2, sticky = tkinter.W)
                    publisher.grid(row = grid_ind, column = 3, sticky = tkinter.W)
                    price.grid(row = grid_ind, column = 4, sticky = tkinter.W)
                    qty.grid(row = grid_ind, column = 5)
            self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =73, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 35)

            self.total_head_summary = tkinter.Label(self.purchase_window_bot, text=("Subtotal(" + str(self.qtytotal) + " books): $" + str(round(self.subtotal, 2))),
                                            font=font_normal, fg=fc_label, bg=bg_label)
            self.total_head_summary.place(x=300, y=10)
            self.backtocatalogue_button = create_button_xy(self.purchase_window_bot, "Back to Catalogue", backtoCatalogue, "TButton", 650, 4, 20)

            self.ship_head = create_label_frame_small(self.purchase_window_bot, "Shipping Address:", True)
            self.ship_name_label = create_label_frame_small(self.purchase_window_bot, "Full Name:", False)
            self.ship_name_entry = create_entry_frame_small(self.purchase_window_bot, width=35)

            self.ship_street_label = create_label_frame_small(self.purchase_window_bot, "Street:", False)
            self.ship_street_entry = create_entry_frame_small(self.purchase_window_bot, width=35)

            self.ship_city_label = create_label_frame_small(self.purchase_window_bot, "City:", False)
            self.ship_city_entry = create_entry_frame_small(self.purchase_window_bot, width=35)

            self.ship_state_label = create_label_frame_small(self.purchase_window_bot, "State:", False)
            self.ship_state_entry = create_entry_frame_small(self.purchase_window_bot, width=35)

            self.ship_country_label = create_label_frame_small(self.purchase_window_bot, "Country:", False)
            self.ship_country_entry = create_entry_frame_small(self.purchase_window_bot, width=35)

            self.ship_zip_label = create_label_frame_small(self.purchase_window_bot, "ZipCode:", False)
            self.ship_zip_entry = create_entry_frame_small(self.purchase_window_bot, width=35)

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
            self.subandtax.place(x=500, y=70)
            self.taxtotal = create_label_frame(self.purchase_window_bot, ("    Total: $" + str(round(self.subtotal, 2)+round(self.subtotal * 0.0625))), 500, 130)

            self.pay_head = create_label_frame_small(self.purchase_window_bot, "Payment Method:", True)
            self.pay_head.place(x=20, y=210)

            self.pay_method = create_label_frame_small(self.purchase_window_bot, self.method, True)
            self.pay_method.place(x=135, y=210)

            self.pay_select_button = create_button_xy(self.purchase_window_bot, "Select Payment Method", selectpayment, "TButton", 40, 235, 20)
            self.confirm_button = create_button_xy(self.purchase_window_bot, "Place Your Order", checkout, "font_normal.TButton", 500, 200, 20)
            self.pur_cancel_button = create_button_xy(self.purchase_window_bot, "Cancel", cancel, "TButton", 555, 240, 15)

            self.payinfo = []           
            
            self.purchase_window_top.place(x=0,y=0)
            self.purchase_window_bot.place(x=0,y=215)
            
            

        self.filterbooks_button = create_button_xy(self.selectbook_window_mid, "Filter the Book Catalogue", filterbooks, "TButton", 300, 50, 30)
        self.filterreset_button = create_button_xy(self.selectbook_window_mid, "Filter Reset", filterreset, "TButton", 528, 25, 15)

        self.bookcatalogue_label = create_label_frame(self.selectbook_window_mid, "Book Catalogue", 340, 90)
        self.title_label = create_label_frame_small(self.selectbook_window_mid, "Title=", False)
        self.title_entry = create_entry_frame_small(self.selectbook_window_mid, width=30)

        self.author_label = create_label_frame_small(self.selectbook_window_mid, "Author=", False)
        self.author_entry = create_entry_frame_small(self.selectbook_window_mid, width=30)

        self.publisher_label = create_label_frame_small(self.selectbook_window_mid, "Publisher=", False)
        self.publisher_entry = create_entry_frame_small(self.selectbook_window_mid, width=30)

        self.price_label = create_label_frame_small(self.selectbook_window_mid, "Price=", False)
        self.price_to = create_label_frame_small(self.selectbook_window_mid, "=<=", False)
        self.price_min_entry = create_entry_frame_small(self.selectbook_window_mid, width=10)
        self.price_max_entry = create_entry_frame_small(self.selectbook_window_mid, width=10)

        self.available_label = create_label_frame_small(self.selectbook_window_mid, "Available=", False)
        self.available_to = create_label_frame_small(self.selectbook_window_mid, "=<=", False)
        self.available_min_entry = create_entry_frame_small(self.selectbook_window_mid, width=10)
        self.available_max_entry = create_entry_frame_small(self.selectbook_window_mid, width=10)

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

        self.total_head = create_label_frame(self.selectbook_window_bot, ("Subtotal(" + str(self.qtytotal) + " books): $" + str(self.subtotal)), 270, 10)
        self.vieworder_button = create_button_xy(self.selectbook_window_bot, "Proceed to Checkout", viewsummary, "font_normal.TButton", 310, 45, 20)
        self.cartreset_button = create_button_xy(self.selectbook_window_bot, "Reset Cart", cartreset, "TButton", 650, 4, 20)
        self.sel_cancel_button = create_button_xy(self.selectbook_window_bot, "Cancel", cancel, "TButton", 365, 90, 15)

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
        self.userinfo_window = create_window(self, "Update User Info", normal_geo)

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
            from main import StoreMainGUI
            StoreMainGUI(self.user_id)
            
        def cancel():
            self.cursor.close()
            self.userinfo_window.destroy()
            from main import StoreMainGUI
            StoreMainGUI(self.user_id)

    #Set the detail appearance
        self.userinfo_head = create_title(self.userinfo_window, "User Info Update", 10)

        self.pass_label = create_label(self.userinfo_window, "Password:", 5, 60)
        self.pass_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

        self.fname_label = create_label(self.userinfo_window, "First Name:", 5, 90)
        self.fname_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

        self.lname_label = create_label(self.userinfo_window, "Last Name:", 5, 120)
        self.lname_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

        self.email_label = create_label(self.userinfo_window, "Email:", 5, 150)
        self.email_entry = tkinter.Entry(self.userinfo_window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=20)

        # Creating buttons
        self.save_button = create_button_xy(self.userinfo_window, "Update Information", edituserinfo, "TButton", 150, 190, 20)
        self.save_button = create_button_xy(self.userinfo_window, "Cancel", cancel, "TButton", 150, 225, 20)

        self.cursor.execute('SELECT * FROM accounts WHERE user_id=?', [self.user_id,])

        # Position the buttons
        self.userdata = self.cursor.fetchone()
                    
        self.pass_entry.insert(0, self.userdata[1])
        self.fname_entry.insert(0, self.userdata[2])
        self.lname_entry.insert(0, self.userdata[3])
        self.email_entry.insert(0, self.userdata[4])
        
        self.pass_entry.place(x=200, y=60)
        self.fname_entry.place(x=200, y=90)
        self.lname_entry.place(x=200, y=120)
        self.email_entry.place(x=200, y=150)


        self.style = ttk.Style()
        self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
        
        #Loop the window
        self.userinfo_window.mainloop()