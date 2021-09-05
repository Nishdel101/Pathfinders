import os
import Tkinter as tk
import ttk


#Buttons


Map = tk.Tk()
frame1 = ttk.Frame(Map)
entry2 = ttk.Entry(frame1)
_text_ = '''Lat here'''
entry2.delete('0', 'end')
entry2.insert('0', _text_)
entry2.place(anchor='nw', relx='0.10', rely='0.43', x='0', y='0')
entry3 = ttk.Entry(frame1)
_text_ = '''Long here'''
entry3.delete('0', 'end')
entry3.insert('0', _text_)
entry3.place(anchor='nw', relx='0.1', rely='0.8', x='0', y='0')
label3 = ttk.Label(frame1)
label3.configure(text='Coordinates')
label3.place(anchor='nw', relx='0.3', rely='0.05', x='0', y='0')
label4 = ttk.Label(frame1)
label4.configure(text='Latitude')
label4.place(anchor='nw', relx='0.1', rely='0.25', x='0', y='0')
label5 = ttk.Label(frame1)
label5.configure(text='Longitude')
label5.place(anchor='nw', relx='0.1', rely='0.65', x='0', y='0')
frame1.configure(height='200', width='200')
frame1.place(anchor='nw', relheight='0.8', relwidth='0.8', relx='0.0', rely='0.0', x='0', y='0')


TLButtonFrame = ttk.Frame(Map)

button1 = ttk.Button(TLButtonFrame)
button1.configure(text='Send Coordinates') #,command= lambda:checkvar1.set(True)
button1.grid(column='0', row='0')
TLButtonFrame.configure(height='30', width='30')
TLButtonFrame.place(anchor='nw', relheight='0.9', relwidth='0.5', relx='0.5', rely='0.8', x='0', y='0')

Map.geometry('300x200')
Map.resizable(True, True)
Map.title('Map')



Map.mainloop()
