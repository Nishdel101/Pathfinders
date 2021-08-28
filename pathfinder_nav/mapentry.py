# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 04:43:36 2021

@author: NDELAVI
"""

import os
import tkinter as tk
import tkinter.ttk as ttk

def Publisher(xCod,yCod):
        print("X-coordinate:",xCod, "Y-coordinate:", yCod)
#Buttons


Map = tk.Tk()
frame1 = ttk.Frame(Map)
xCod = ttk.Entry(frame1)
_text_ = '''Lat here'''
xCod.delete('0', 'end')
xCod.insert('0', _text_)
xCod.place(anchor='nw', relx='0.10', rely='0.43', x='0', y='0')
yCod = ttk.Entry(frame1)
_text_ = '''Long here'''
yCod.delete('0', 'end')
yCod.insert('0', _text_)
yCod.place(anchor='nw', relx='0.1', rely='0.8', x='0', y='0')
label1 = ttk.Label(frame1)
label1.configure(text='Coordinates')
label1.place(anchor='nw', relx='0.3', rely='0.05', x='0', y='0')
label2 = ttk.Label(frame1)
label2.configure(text='Latitude')
label2.place(anchor='nw', relx='0.1', rely='0.25', x='0', y='0')
label3 = ttk.Label(frame1)
label3.configure(text='Longitude')
label3.place(anchor='nw', relx='0.1', rely='0.65', x='0', y='0')
frame1.configure(height='200', width='200')
frame1.place(anchor='nw', relheight='0.8', relwidth='0.8', relx='0.0', rely='0.0', x='0', y='0')


TLButtonFrame = ttk.Frame(Map)

button1 = ttk.Button(TLButtonFrame)
button1.configure(text='Send Coordinates', command= lambda:Publisher(xCod.get(),yCod.get()))
button1.grid(column='0', row='0')
TLButtonFrame.configure(height='30', width='30')
TLButtonFrame.place(anchor='nw', relheight='0.9', relwidth='0.5', relx='0.5', rely='0.8', x='0', y='0')

Map.geometry('300x200')
Map.resizable(True, True)
Map.title('Map')



Map.mainloop()
