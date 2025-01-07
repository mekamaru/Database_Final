#test file

import tkinter
from tkinter import ttk #Ttk widgets gives the application an improved look and feel
from tkinter import messagebox
import sqlite3
import os
import sys

from variables import *

class test:

    def __init__(self):

        self.m_window = create_window(self, "User Login", normal_geo)

        self.m_window.mainloop()

test()
