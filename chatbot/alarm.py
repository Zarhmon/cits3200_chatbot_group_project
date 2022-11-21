import datetime
from tkinter import *
from tkinter import messagebox
import threading
import time

alarm_msg = ""

def launchAlarm(msg, mins):

    global alarm_msg
    alarm_msg = msg
    print(alarm_msg)

    try:
        minutes = mins
        print("minutes",minutes)
        if minutes < 0:
            messagebox.showinfo(message="Invalid time")
            raise ValueError()

        threading.Timer(
            interval = float(mins)*60, 
            function = create_popup
        ).start()
        
    
    except ValueError:
        messagebox.showinfo(message="Error.., n >= 0, and n cannot be decimal (e.g. 0.1)")

def create_popup():
    print("creating popup")
    messagebox.showinfo(title="Reminder", message=alarm_msg)


if __name__ == "__main__":    
    ala = launchAlarm()
    ala.on_check()


    
    