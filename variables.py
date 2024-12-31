
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
list_w = 1920
list_h = 1080
list_geo = f"{list_w}x{list_h}"
print(normal_geo)

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

def create_label(window: tkinter.Tk, title: str, x: int, y: int):
    label = tkinter.Label(window, text = title, font=font_normal_bold, fg=fc_label, bg=bg_label)
    label.place(x=x, y=y)

    return label

def create_title(window: tkinter.Tk, title: str, y: int):
    label = tkinter.Label(window, text = title, font=font_normal_bold, fg=fc_label, bg=bg_label)
    label.place(relx = 0.5, y=y, anchor = 'center')

    return label

def create_entry(window: tkinter.Tk, x: int, y: int, width: int):
    entry = tkinter.Entry(window, bd=1, font=font_normal, fg=fc_entry, bg=bg_entry, width=width)
    entry.place(x=x, y=y)

    return entry

def create_button_xy(window: tkinter.Tk, title: str, command: Callable[[], None], style: str, x: int, y: int, width: int):
    button = ttk.Button(window, command = command, text = title, style = style, width = width)
    button.place(x = x, y = y)

    return button

def create_button_center(window: tkinter.Tk, title: str, command: Callable[[], None], style: str, y: int, width: int):
    button = ttk.Button(window, command = command, text = title, style = style, width = width)
    button.place(relx=0.5, y = y, anchor='center')

    return button
