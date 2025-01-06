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


class ViewOrderGUI():
    def __init__(self): #storemainGUI()に呼び出されるGUIは全部user_idを参照する
        self.cursor = db.cursor()

    #Set the appearance
        self.vieworder_window = create_window(self, "View Order", multiframe_geo) #bookcatalogue一覧から選ぶ -> 選択画面がメインウィンドウのGUI(user_id)

        self.vieworder_window_top = tkinter.Frame(height = 40, width = multiframe_w, bg = bg_normal) #カタログのフィルタリング →第二フレーム
        self.vieworder_window_bot = tkinter.Frame(height = 40, width = multiframe_w, bg = bg_normal) #合計金額の計算　→　第三フレーム
        self.vieworder_detail_bot = tkinter.Frame(height=40, width = 820, bg = bg_normal) #支払い方法の入力　→　オーバーｒｙその③

        # Creating the frame for list view (as same as book list in BuyBookGUI)
        
        #一覧スクロール　→　メインに直付け・第一フレーム（キャンバス内）

        # Scrollbar を生成して配置
        self.canvas = tkinter.Canvas(self.vieworder_window, bg =bg_normal, height = 460, width= multiframe_w)
        self.bar = tkinter.Scrollbar(self.vieworder_window, orient=tkinter.VERTICAL)
        
        self.bar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.bar.set)
        
    #Set the actions
        def cancel():
             self.cursor.close()
             self.vieworder_window.destroy()
             from main import AdminGUI
             AdminGUI()
        
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

                info = create_label_frame_small(self.vieworder_detail, txt)
                info.place(x=0,y=0)
                self.canvas.config(scrollregion=(0,0,50,len(booklist)*30))
                self.vieworder_detail.config(height = len(booklist)*30)
                self.bar.pack(side=tkinter.RIGHT,  pady=0, ipady =0, fill =tkinter.Y)
                self.canvas.pack(side=tkinter.TOP, pady=0)

                self.backtolist_button = create_button_xy(self.vieworder_detail_bot, "Back to View Order", backtolist, "TButton", 300, 5, 20)
                self.vieworder_detail_bot.place(x=0,y=460)
            
            self.var = tkinter.IntVar(value = 0)
            self.orderlist = tkinter.Frame(self.canvas,height = 460, width = multiframe_w, bg = bg_label)
            self.canvas.config(height = 420)
            self.canvas.create_window((0,0), window=self.orderlist, anchor=tkinter.NW, width=self.canvas.cget('width'))
            self.selectedorders = conn.fetchall()
            self.canvas.config(scrollregion=(0,0,50,1000 + len(self.selectedorders)*30)) #スクロール範囲

            oid_head = create_label_frame_small(self.orderlist, "Order ID")
            uid_head = create_label_frame_small(self.orderlist, "User ID")
            qty_head = create_label_frame_small(self.orderlist, "Total Qty")
            price_head = create_label_frame_small(self.orderlist, "Total Price")
            method_head = create_label_frame_small(self.orderlist, "Payment Method")
            detail_head = create_label_frame_small(self.orderlist, "Show Detail")

            oid_head.grid(row = 0, column = 1)
            uid_head.grid(row = 0, column = 2)
            qty_head.grid(row = 0, column = 3)
            price_head.grid(row = 0, column = 4)
            method_head.grid(row = 0, column = 5)
            detail_head.grid(row = 0, column = 6)
            
            for order in self.selectedorders:
                print(str(order[0]))
                oid = create_label_frame_small(self.orderlist, str(order[0]))
                uid = create_label_frame_small(self.orderlist, str(order[1]))
                qty = create_label_frame_small(self.orderlist, str(sum([int(x) for x in order[2].split(":")])))
                price = create_label_frame_small(self.orderlist, ("$" +str(order[3])))
                method = create_label_frame_small(self.orderlist, str(order[5].split(":")[0]))
                detail = tkinter.Radiobutton(self.orderlist, variable=self.var, value=int(order[0]), command = viewdetail, fg=fc_label, bg=bg_label)
                detail.deselect()

                grid_row = int(order[0]) + 1
                oid.grid(row = grid_row, column = 1, sticky = tkinter.W)
                uid.grid(row = grid_row, column = 2, sticky = tkinter.W)
                qty.grid(row = grid_row, column = 3, sticky = tkinter.W)
                price.grid(row = grid_row, column = 4, sticky = tkinter.W)
                method.grid(row = grid_row, column = 5, sticky = tkinter.W)
                detail.grid(row = grid_row, column = 6)

            self.bar.pack(side=tkinter.RIGHT, pady=30, ipady =195, anchor = tkinter.N)
            self.canvas.pack(side=tkinter.TOP, pady = 35)

            self.vieworder_head = create_label_frame(self.vieworder_window_top, "View Order", 360, 0)
            self.vieworder_window_top.place(x=0,y=0)

            self.cancel_button = ttk.Button(self.vieworder_window_bot, command=cancel, text="Cancel", style="TButton", width=15)
            self.cancel_button = create_button_xy(self.vieworder_window_bot, "Cancel", cancel, "TButton", 325, 3, 15)
            self.vieworder_window_bot.place(x=0,y=460)
            
            

        createorderslist(self.cursor.execute('SELECT * FROM orders'))

# class ViewOrderGUI:
#     def __init__(self):
#         # Set the cursor for db
#         self.cursor = db.cursor()
    
#         # Set the appearance of the main window
#         self.vieworder_window = create_window(self, "View Order", list_geo)
    
#         # Create frames
#         self.vieworder_window_top = tkinter.Frame(height=680, width=1000, bg=bg_normal)
#         self.vieworder_window_bot = tkinter.Frame(height=100, width=list_w, bg=bg_normal)
#         self.vieworder_detail_bot = tkinter.Frame(height=100, width=list_w, bg=bg_normal)

#         # Canvas setup
#         self.canvas_h = 680
#         self.canvas_w = 1000
#         self.canvas = tkinter.Canvas(self.vieworder_window, bg=bg_normal, height=self.canvas_h, width=self.canvas_w)
#         self.bar = tkinter.Scrollbar(self.vieworder_window, orient=tkinter.VERTICAL)
#         self.bar.config(command=self.canvas.yview)
#         self.canvas.config(yscrollcommand=self.bar.set)
    
#         def cancel():
#             self.cursor.close()
#             self.vieworder_window.destroy()
#             from main import AdminGUI
#             AdminGUI()
    
#         def createorderslist(order_list):
#             def viewdetail():
#                 def backtolist():
#                     self.vieworder_detail.destroy()
#                     self.vieworder_detail_bot.place_forget()
#                     createorderslist(self.cursor.execute('SELECT * FROM orders'))

#                 self.orderlist_frame.destroy()
#                 self.vieworder_detail = tkinter.Frame(self.canvas, height=self.canvas_h, width=self.canvas_w, bg=bg_label)
#                 self.canvas.create_window((0, 0), window=self.vieworder_detail, anchor=tkinter.N, width=self.canvas.cget('width'))
#                 self.canvas.config(height=self.canvas_h, width=self.canvas_w)

#                 # Create the order details
#                 txt = ("Order Detail\n===================================================================")
#                 order = self.cursor.execute('SELECT * FROM orders WHERE order_id =?', [self.var.get(),]).fetchone()
#                 booklist = [int(x) for x in order[2].split(":")]
#                 for i in range(0, len(booklist)):
#                     if booklist[i] != 0:
#                         book = self.cursor.execute('SELECT * FROM books WHERE book_id =?', [i,]).fetchone()
#                         txt += ("\nTitle: " + str(book[1]) + "\nAuthor: " + str(book[2]) + "\nPublisher: " + str(book[3])
#                                  + "\nPrice: " + str(book[4]) + "\nQty: " + str(booklist[i]))
#                         txt += "\n==================================================================="

#                 # Customer Information
#                 txt += "\nCustomer Information:\n==================================================================="
#                 shipinfo = order[4].split(":")
#                 txt += ("\nFull Name: " + str(shipinfo[0]) +
#                         "\nShipping Address:\n Street: " + str(shipinfo[1]) +
#                         "\n City: " + str(shipinfo[2]) +
#                         "\n State: " + str(shipinfo[3]) +
#                         "\n Country: " + str(shipinfo[4]) +
#                         "\n Zip: " + str(shipinfo[5]))

#                 # Payment Information
#                 txt += "\nPayment Information:\n==================================================================="
#                 payinfo = order[5].split(":")
#                 txt += "\nPayment Method: " + str(payinfo[0])
#                 if payinfo[0] == "Credit/Debit Card":
#                     txt += ("\nName on Card: " + str(payinfo[2]) +
#                             "\nCard Number: " + str(payinfo[3]) +
#                             "\nCard Exp: " + str(payinfo[4]) + "/" + str(payinfo[5]) +
#                             "\nBilling Address:\n Street: " + str(payinfo[6]) +
#                             "\n City: " + str(payinfo[7]) +
#                             "\n State: " + str(payinfo[8]) +
#                             "\n Country: " + str(payinfo[9]) +
#                             "\n Zip: " + str(payinfo[10]) +
#                             "\n Phone: " + str(payinfo[11]))
#                 elif payinfo[0] == "Bank Check":
#                     txt += ("\nName: " + str(payinfo[2]) +
#                             "\nBank Type: " + str(payinfo[3]) +
#                             "\nRouting Number: " + str(payinfo[4]) +
#                             "\nAccount Number: " + str(payinfo[5]))
#                 else:
#                     txt += "\nYou must pay when you receive the box."

#                 # Display the text in the frame
#                 info = create_head(self.vieworder_detail, txt)
#                 info.place(relx=0.5, y=0, anchor='center')

#                 # Adjust canvas scroll region
#                 self.canvas.config(scrollregion=(0, 0, 50, len(booklist) * 30))
#                 self.vieworder_detail.config(height=len(booklist) * 30)
#                 self.bar.pack(side=tkinter.RIGHT, pady=0, ipady=0, fill=tkinter.Y)
#                 self.canvas.pack(side=tkinter.TOP, pady=0)

#                 # Add back button
#                 self.backtolist_button = create_button_center(self.vieworder_detail_bot, "Back to View Order", backtolist, "TButton", 30, 20)
#                 self.vieworder_detail_bot.place(x=0, y=self.canvas_h)
#                 self.vieworder_detail_bot.lift()

#             # # Create order list frame
#             # self.var = tkinter.IntVar(value=0)
#             self.orderlist_frame = tkinter.Frame(self.canvas, height=self.canvas_h, width=self.canvas_w, bg=bg_label)
#             # self.canvas.create_window((0, 0), window=self.orderlist_frame, anchor=tkinter.NW, width=self.canvas.cget('width'))
#             # self.selectedorders = order_list.fetchall()

#             # # Set canvas scroll region
#             # self.canvas.config(scrollregion=(0, 0, 50, 1000 + len(self.selectedorders) * 30))

#             # # Create header row
#             # headers = ["Order ID", "User ID", "Total Qty", "Total Price", "Payment Method", "Show Detail"]
#             # for i in range(len(headers)):
#             #     create_head(self.orderlist_frame, text=headers[i]).grid(row=0, column=i + 1)
            
#             # ind = 1  # Start the index from 1 for the first row of orders
#             # for order in self.selectedorders:
#             #     oid = create_head(self.orderlist_frame, text=str(order[0]))
#             #     uid = create_head(self.orderlist_frame, text=str(order[1]))
#             #     qty = create_head(self.orderlist_frame, text=str(sum([int(x) for x in order[2].split(":")])))
#             #     price = create_head(self.orderlist_frame, text=f"${order[3]}")
#             #     method = create_head(self.orderlist_frame, text=order[5].split(":")[0])

#             #     # Create radiobutton for viewing details
#             #     detail = tkinter.Radiobutton(self.orderlist_frame, variable=self.var, value=int(order[0]), command=viewdetail, fg=fc_label, bg=bg_label)
#             #     detail.deselect()

#             #     # Position order items in grid
#             #     oid.grid(row=ind, column=1, sticky=tkinter.W)
#             #     uid.grid(row=ind, column=2, sticky=tkinter.W)
#             #     qty.grid(row=ind, column=3, sticky=tkinter.W)
#             #     price.grid(row=ind, column=4, sticky=tkinter.W)
#             #     method.grid(row=ind, column=5, sticky=tkinter.W)
#             #     detail.grid(row=ind, column=6)

#             #     ind = ind + 1

#             #  # Add scrollbar and canvas to the window
#             # self.bar.pack(side=tkinter.RIGHT, pady=30, ipady=195, anchor=tkinter.N)
#             # self.canvas.pack(side=tkinter.TOP, pady=35)

#             # # Create and place title and cancel button
#             # self.vieworder_title = create_title(self.vieworder_window_top, "View Order", 10)
#             # self.vieworder_window_top.place(x=0, y=0)

#             # self.cancel_button = create_button_center(self.vieworder_window_bot, "Cancel", cancel, "TButton", 30, 15)
#             # self.vieworder_window_bot.place(x=0, y=self.canvas_h)
#             # self.vieworder_window_bot.lift()

#             #create canvas
#             canvas = tkinter.Canvas(self.vieworder_window_top, bg = bg_normal, height = 680, width = 1000, scrollregion = (0, 0, 1000, len(order_list)*30))
    
#             #create scroll bar
#             bar = tkinter.Scrollbar(self.vieworder_window_top, orient = tkinter.VERTICAL, command = canvas.yview)
#             bar.pack(side = tkinter.RIGHT, pady = 30, ipady = 420, anchor = tkinter.N)

#             #set the scrollable area
#             canvas.config(yscrollcommand = bar.set)

#             #create frame widget on canvas and place the frame on canvas
#             frame = tkinter.Frame(canvas)
#             canvas.create_window((0, 0), window = frame, anchor = tkinter.NW, width = canvas.cget('width'))

#             # Create header row
#             headers = ["Order ID", "User ID", "Total Qty", "Total Price", "Payment Method", "Show Detail"]
#             for i in range(len(headers)):
#                 create_head(self.orderlist_frame, text=headers[i]).grid(row=0, column=i + 1)

#             #create multiple button widgets and place them on frame
#             var = tkinter.IntVar()
#             for order in order_list:

#                 oid = create_head(self.orderlist_frame, text=str(order[0]))
#                 uid = create_head(self.orderlist_frame, text=str(order[1]))
#                 qty = create_head(self.orderlist_frame, text=str(sum([int(x) for x in order[2].split(":")])))
#                 price = create_head(self.orderlist_frame, text=f"${order[3]}")
#                 method = create_head(self.orderlist_frame, text=order[5].split(":")[0])

#                 # Create radiobutton for viewing details
#                 detail = tkinter.Radiobutton(self.orderlist_frame, variable=var, value=int(order[0]), command=viewdetail, fg=fc_label, bg=bg_label)
#                 detail.deselect()

#                 ind = int(order[0]) + 1
#                 # Position order items in grid
#                 oid.grid(row=ind, column=1, sticky=tkinter.W)
#                 uid.grid(row=ind, column=2, sticky=tkinter.W)
#                 qty.grid(row=ind, column=3, sticky=tkinter.W)
#                 price.grid(row=ind, column=4, sticky=tkinter.W)
#                 method.grid(row=ind, column=5, sticky=tkinter.W)
#                 detail.grid(row=ind, column=6)
        
#             #place the canvas on the window
#             canvas.pack(side = tkinter.TOP, pady = 50)

#             # Wait for a selection
#             self.vieworder_window_top.wait_variable(var)
#             canvas.destroy()

#             # Create and place title and cancel button
#             self.vieworder_title = create_title(self.vieworder_window_top, "View Order", 10)
#             self.vieworder_window_top.place(x=0, y=0)

#             self.cancel_button = create_button_center(self.vieworder_window_bot, "Cancel", cancel, "TButton", 30, 15)
#             self.vieworder_window_bot.place(x=0, y=self.canvas_h)
#             self.vieworder_window_bot.lift()

#         self.cursor.execute('SELECT * FROM orders')
#         createorderslist(self.cursor.fetchall())
        #Create labels and entries
    
        #Set the actions on this GUI
    
        #Create buttons
    
        #Loop the window