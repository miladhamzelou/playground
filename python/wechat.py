# pip install itchat
# pyinstaller -F -w -i manage.ico app.py

import itchat
import tkinter as tk
from tkinter.ttk import *
from tkinter import *
import easygui as g
import filetype
import os

root = tk.Tk()
root.title('微信文件传输系统')
cv = Canvas(root, width=200, height=200, bg="white")
cv.pack()

frame = Frame(root)
frame.pack()


def login():
    itchat.auto_login(hotReload=True)


def open():
    QRurl = g.fileopenbox('选择文件', '提示', default='*', filetypes=['*.py'])
    itchat.send_file(QRurl, toUserName="urugang")


Button1 = Button(root, text="打开/发送文件", font=("仿宋", 14, "bold"), command=open)
cv.create_window(20, 100, anchor=NW, window=Button1)
Button1 = Button(root, text="登录微信", font=("仿宋", 14, "bold"), command=login)
cv.create_window(20, 40, anchor=NW, window=Button1)
root.mainloop()
