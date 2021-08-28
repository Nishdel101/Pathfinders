#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
import tkinter as tk
import tkinter.ttk as ttk

rospy.init_node('goal_publisher', anonymous=True)

goal = PoseStamped()

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped)


def goal_message(x_goal, y_goal):
    goal.header.stamp = rospy.get_rostime()
    goal.header.frame_id = 'map'

    goal.pose.position.x = x_goal
    goal.pose.position.y = y_goal
    goal.pose.position.z = 0.0

    goal.pose.orientation.w = 1.0
    goal.pose.orientation.x = 0.0
    goal.pose.orientation.y = 0.0
    goal.pose.orientation.z = 0.0

    pub.publish(goal)


# Buttons


Map = tk.Tk()
frame1 = ttk.Frame(Map)
xCod = ttk.Entry(frame1)
_text_ = ''
xCod.delete('0', 'end')
xCod.insert('0', _text_)
xCod.place(anchor='nw', relx='0.10', rely='0.43', x='0', y='0')
yCod = ttk.Entry(frame1)
_text_ = ''
yCod.delete('0', 'end')
yCod.insert('0', _text_)
yCod.place(anchor='nw', relx='0.1', rely='0.8', x='0', y='0')
label1 = ttk.Label(frame1)
label1.configure(text='Coordinates')
label1.place(anchor='nw', relx='0.3', rely='0.05', x='0', y='0')
label2 = ttk.Label(frame1)
label2.configure(text='x:')
label2.place(anchor='nw', relx='0.1', rely='0.25', x='0', y='0')
label3 = ttk.Label(frame1)
label3.configure(text='Y:')
label3.place(anchor='nw', relx='0.1', rely='0.65', x='0', y='0')
frame1.configure(height='200', width='200')
frame1.place(anchor='nw', relheight='0.8', relwidth='0.8', relx='0.0', rely='0.0', x='0', y='0')


TLButtonFrame = ttk.Frame(Map)

button1 = ttk.Button(TLButtonFrame)
button1.configure(text='Send Coordinates', command=lambda: goal_message(float(xCod.get()), float(yCod.get())))
button1.grid(column='0', row='0')
TLButtonFrame.configure(height='30', width='30')
TLButtonFrame.place(anchor='nw', relheight='0.9', relwidth='0.5', relx='0.5', rely='0.8', x='0', y='0')

Map.geometry('300x200')
Map.resizable(True, True)
Map.title('Map')


Map.mainloop()
