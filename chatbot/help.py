from tkinter import *
import tkinter

def launchHelp():
    root = Tk()
    root.wm_attributes('-topmost',1)
    root.title("Instructions")

    text = tkinter.Text(root, height=30, width=60, wrap="none")

    xscrollbar = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
    xscrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

    yscrollbar = tkinter.Scrollbar(root)
    yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    text.pack(side=tkinter.LEFT)

    yscrollbar.config(command=text.yview)
    text.config(yscrollcommand=yscrollbar.set)

    xscrollbar.config(command=text.xview)
    text.config(xscrollcommand=xscrollbar.set)

    str = """   Instructions:\n\n
    I can translate over 100 languages! Try it by starting a sentence with the word 'Translate' followed by another language!\n
    ------------------------------------\n
    I can tell you the weather of any place in the world! Try it by asking me 'What is the weather in Perth'!!\n
    ------------------------------------\n
    Do you want to know where something is? Ill tell you if you start a question with 'Where is' and the place you want to know!\n
    ------------------------------------\n
    If im annoying you, you can press the Hush button in the drop down menu at the top to make me go to sleep. I'll miss talking with you though.\n
    ------------------------------------\n
    Do you want to know your friends phone number? Ask me a question with 'Get contact' followed by their name and I will try my best to get it!\n
    ------------------------------------\n
    I can check your calendar for you! Ask me 'What is coming up' and I will list the next 10 things in your calender!\n
    ------------------------------------\n
    I can add things to your calendar, just ask me 'Add to calendar, event, date, time' and I'll do it for you!\n
    ------------------------------------\n
    Do you want to hear a joke? If so just ask me to tell you a joke! I even tell dad or computting jokes, just ask!\n
    ------------------------------------\n
    I can set a timer for you! Just go to the drop down menu at the top and select 'Alarm'.\n  
    ------------------------------------\n
    """
    text.insert(tkinter.END, str)
    root.mainloop()

if __name__ == "__main__":   
    launchHelp()