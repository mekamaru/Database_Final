
import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
from typing import Callable
import sqlite3
import os
import sys

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
fg_logout = "#C32148"

#size
normal_w = 520
normal_h = 300
normal_geo = f"{normal_w}x{normal_h}"
list_w = 1520
list_h = 800
list_geo = f"{list_w}x{list_h}+0+0"

#set database
db=sqlite3.connect("bookstore.db")

def on_closing(window: tkinter.Tk):
    window.destroy()
    db.close()
    print("Closing!: test")
    sys.exit()

def create_window(self, title: str, geo: str):
    self.window = tkinter.Tk()
    self.window.title(title)
    self.window.geometry(geo)
    self.window.config(bg=bg_normal)
    self.window.protocol("WM_DELETE_WINDOW", lambda: on_closing(self.window))

    self.style = ttk.Style()
    self.style.configure("TButton", font=font_normal, foreground=fg_button, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
    self.style.configure("logout.TButton", font=font_normal, foreground=fg_logout, background=bg_button, activeforeground=bg_entry, activebackground=fg_button)
    return self.window

def create_label(window: tkinter.Tk, #Window for placing this label
                 text: str,          #This label's text
                 x: int,             #X value for placing this label
                 y: int              #Y value for placing this label
                 ): 
    label = tkinter.Label(window, text = text, font=font_normal_bold, fg=fc_label, bg=bg_label)
    label.place(x=x, y=y)

    return label

def create_title(window: tkinter.Tk, #Window for placing this title label
                 title: str,         #This title label's text
                 y: int              #Y value for placing this label
                 ):
    label = tkinter.Label(window, text = title, font=font_normal_bold, fg=fc_label, bg=bg_label)
    label.place(relx = 0.5, y=y, anchor = 'center')

    return label

def create_entry(window: tkinter.Tk, #Window for placing this entry box
                 x: int,             #X value for placing this entry box
                 y: int,             #Y value for placing this entry box
                 width: int          #Width of this entry box
                 ):
    entry = tkinter.Entry(window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=width)
    entry.place(x=x, y=y)

    return entry

def create_button_xy(window: tkinter.Tk,          #Window for placing this button
                     title: str,                  #This button's title
                     command: Callable[[], None], #The command when this button is pushed
                     style: str,                  #Style of this button
                     x: int,                      #X value for placing this button
                     y: int,                      #Y value for placing this button
                     width: int                   #Width of this button
                     ):
    button = ttk.Button(window, command = command, text = title, style = style, width = width)
    button.place(x = x, y = y)

    return button

def create_button_center(window: tkinter.Tk,          #Window for placing this button
                         title: str,                  #This button's title
                         command: Callable[[], None], #The command when this button is pushed
                         style: str,                  #Style of this button
                         y: int,                      #Y value for placing this button
                         width: int                   #Width of this button
                         ):
    button = ttk.Button(window, command = command, text = title, style = style, width = width)
    button.place(relx=0.5, y = y, anchor='center')

    return button


def create_scroll(window: tkinter.Tk,     #Window for placing this scroll canvas
                  canvas_height: int,     #Height of this scroll canvas
                  canvas_width: int,      #Width of this scroll canvas
                  bar_pady: int,          #pady value of scroll bar
                  bar_ipady: int,         #ipady value of scroll bar
                  item_list: list[tuple], #Item list for scroll canvas
                  item_type: str          #Item type
                  ):
    #create canvas
    canvas = tkinter.Canvas(window, bg = bg_normal, height = canvas_height, width = canvas_width, scrollregion = (0, 0, canvas_width, len(item_list)*25))
    
    #create scroll bar
    bar = tkinter.Scrollbar(window, orient = tkinter.VERTICAL, command = canvas.yview)
    bar.pack(side = tkinter.RIGHT, pady = bar_pady, ipady = bar_ipady, anchor = tkinter.N)

    #set the scrollable area
    canvas.config(yscrollcommand = bar.set)

    #create frame widget on canvas and place the frame on canvas
    frame = tkinter.Frame(canvas)
    canvas.create_window((0, 0), window = frame, anchor = tkinter.NW, width = canvas.cget('width'))

    def set_id():
        canvas.destroy()
        return var.get()

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

    #create multiple button widgets and place them on frame
    var = tkinter.IntVar()
    ids = []
    ind = 0
    for item in item_list:

        ids.append(item[0])

        #change the text depend on item type
        if item_type == "user":
            text = ("UserID: %s"%str(item[0])+
                    "/ Password: %s"%str(item[1])+
                    "/ Firstname: %s"%str(item[2])+
                    "/ Lastname: %s"%str(item[3])+
                    "/ Email: %s"%str(item[4])+
                    "/ Payment method: %s"%str(convertpayment(item[5]))
                    )
        elif item_type == "book":
            text = ("BookID: %s"%str(item[0])+ 
                    "/ Title: %s"%str(item[1])+
                    "/ Author: %s"%str(item[2])+
                    "/ Publisher: %s"%str(item[3])+
                    "/ Price: %s"%str(item[4])+
                    "/ Availability: %s"%str(item[5])
                    )
        else:
            text = "No Data"

        bt = tkinter.Radiobutton(frame, text = text, bg = bg_normal, variable = var, value = ind, anchor = 'w')
        ind = ind + 1
        bt.pack(fill=tkinter.X)
        
    #place the canvas on the window
    canvas.pack(side = tkinter.TOP, pady = 50)

    # Wait for a selection
    window.wait_variable(var)
    canvas.destroy()
    return ids[var.get()]

    

