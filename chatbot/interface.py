
from ctypes import resize
from tkinter import *
import tkinter as tk
from itertools import cycle
import tkinter
from PIL import ImageTk, Image
import python_avatars as pa
import time 
import random
import pyvips
from os.path import exists
import aboutus
import help
import threading
from threading import Thread
import webbrowser
from functools import partial
import __init__

# Multiple maps global var./list
imglist = []
count = 0

#======================= Setting Fonts =================================================# 
set_font = ("Roboto", 10) # setting default font style and size

bold_font = ("Roboto", 11, "bold") # change style to bold

def create_window(getReply, account):

#================== Defining Functions =================================================# 

    # function to call google login and change to frame 2
    def submit_button():
        message_window.bind('<Return>', send)
        account.login()
        show_frame(frame2)

    # function to call frame swapping
    def show_frame(frame):
        message_window.configure(state="normal") # allows users to type into frame 2 message_window when frame 2 is called
        frame.tkraise() # brings new frame to the front
    
    # function to clear window on log out
    def clear_chat_window():
        chat_window.configure(state="normal")
        message_window.unbind('<Return>')
        chat_window.delete("1.0", END) # clears chat_window after msg is sent
        chat_window.configure(state="disabled") # disables users for inputting directly into window
        message_window.configure(state="disabled") # disables users from typing into frame 2 while frame 1 is displayed

    def chat_window_state():
        message_window.configure(state="normal")
        message_window.bind('<Return>', send)

    # send message function for frame2

    def send(input):    
        msg = message_window.get("1.0", END).strip()
        lowermsg = msg.lower()
        if len(msg) == 0:
            print("message_window is empty")
            return 'break'  # stops the return key from starting new line in message_window
        else:
            reply = getReply(msg)
            print(f"User: {msg}")
            print(f"Bot: {reply}")
            chat_window.configure(state="normal") # allows inserting into window
            chat_window.insert(END, f"\nUser \n{msg}\n")
            # chat_window.tag_configure("right", justify='right') # configures window to input text right alligned
            # chat_window.tag_add("right", 50.50, "end")

            if (lowermsg.startswith("where is")):
                global count
                global map_image 
                global imglist
                chat_window.insert(END, f"\nAssistant \nThe closest result is ")
                url = reply
                chat_window.insert(END,"here",hyperlink.add(partial(webbrowser.open, url)))
                chat_window.insert(END, "\n\n")
        
                map_image = PhotoImage(file='msc/map_sc'+str(count)+'.png') # importing the image, need to add image resizing
                imglist.append(map_image)
                chat_window.image_create(END, image=imglist[count])
                count=count+1

            elif ("scholar search" in lowermsg):
                chat_window.insert(END, f"\nAssistant \n")
                for item in reply:
                    chat_window.insert(END,item["title"],hyperlink.add(partial(webbrowser.open, item["link"])))


            elif ("search" in lowermsg):
                chat_window.insert(END, f"\nAssistant \n")
                for i,item in enumerate(reply):
                    chat_window.insert(END, f"{i+1}. ")
                    chat_window.insert(END,f"{item['title']}\n",hyperlink.add(partial(webbrowser.open, item["link"])))
            else:
                chat_window.insert(END, f"\nAssistant \n{reply}\n")
                print("\n")
            chat_window.configure(state="disabled") # disables users for inputting directly into window
            chat_window.see(tk.END) # moves scroll bar to latest message location
            message_window.delete("1.0", END) # clears message_window after msg is sent
            return 'break'  # stops the return key from starting new line in message_window

    def hush(): 
        print("Assistant is now hushed")
        root_window.wm_state('iconic')
        # time.sleep(10)
        
    def focus_window(): # import to open window
        root_window.wm_state('normal')

    #================== Creating Root Window =================================================#    
    root_window = tk.Tk()
    root_window.title("YuBot") # window name
    root_window.geometry("400x500+50+50") # dimensions + Location; Width x Height + x + y axis
    root_window.resizable(width=False, height=False) # disable window resize
    root_window.rowconfigure(0, weight=1) # configuring window rows
    root_window.columnconfigure(0, weight=1) # configuring window columns

    # creating login frame1 & chatbot frame2
    frame1 = tk.Frame(root_window, bg= '#FFFFFF') #4F415A
    frame2 = tk.Frame(root_window, bg= '#FFFFFF') #3E4971

    # cycling the frames 
    for frame in (frame1, frame2):
        frame.grid(row=0,column=0,sticky='nsew')
        
    #================== Frame 1 - Avatar creation code ======================================================#
  
    # Background lbl 
    bg_lbl = tk.Label(frame1, bg='#84CBEE')
    bg_lbl.place(x=6, y=6, height= 488, width= 388)
    # top text label
    text_lbl = tk.Label(frame1, bg='#84CBEE', text= "Hi, I am your assistant!", font=bold_font)
    text_lbl.place(x=7, y=7, height = 25, width = 386)

    # Inserting avatar image
    def insert_img():
        av_bdr =tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0) # creating avatar border
        av_bdr.place(x=124, y=34, height=202, width=152)
        if exists('my_avatar.png'):
            photo = Image.open('my_avatar.png') # importing the image
        else:
            photo = Image.open('generic_avatar.png') # importing the image
        resize_img = photo.resize((200, 200), Image.LANCZOS) # resizing 
        img = ImageTk.PhotoImage(resize_img)
        av_lbl = tk.Label(frame1) # creating image label
        av_lbl.image =img # saving reference of photo 
        av_lbl.place(x=125, y=35, height=200, width=150) # placing the image label
        av_lbl.configure(image=img) # setting the label to the image

    insert_img()

    # Creating avatar elemnt types
    list_skin_color = cycle(['TANNED','YELLOW','PALE','LIGHT','BROWN','DARK_BROWN','BLACK'])
    list_eye_type = cycle(['CLOSED', 'CRY', 'DEFAULT', 'EYE_ROLL', 'HAPPY', 'HEART', 'SIDE', 'SQUINT', 'SURPRISED', 'WINK_WACKY', 'WINK', 'X_DIZZY'])
    list_top_type = cycle(['NONE', 'BIG_HAIR', 'BOB', 'BUN', 'CURLY', 'CURVY', 'DREADS', 'FRIDA', 'FRIZZLE', 'FRO_BAND', 'FRO', 'LONG_NOT_TOO_LONG', 'SHAGGY_MULLET', 'SHAGGY', 'SHAVED_SIDES', 'SHORT_CURLY', 'SHORT_DREADS_1', 'SHORT_DREADS_2', 'SHORT_FLAT', 'SHORT_ROUND', 'SHORT_WAVED', 'SIDES', 'STRAIGHT_1', 'STRAIGHT_2', 'STRAIGHT_STRAND'])
    list_mouth_type = cycle(['DEFAULT','CONCERNED','DISBELIEF','EATING','GRIMACE','SAD','SCREAM_OPEN','SERIOUS','SMILE','TONGUE','TWINKLE','VOMIT'])
    list_accessories_type = cycle(['NONE', 'KURT','ROUND','SUNGLASSES','WAYFARERS'])
    list_clothe_type = cycle(['BLAZER_SHIRT','BLAZER_SWEATER','COLLAR_SWEATER','GRAPHIC_SHIRT','HOODIE','OVERALL','SHIRT_CREW_NECK','SHIRT_SCOOP_NECK','SHIRT_V_NECK'])
    list_facial_hair_type = cycle(['NONE', 'BEARD_LIGHT', 'BEARD_MAGESTIC', 'BEARD_MEDIUM', 'MOUSTACHE_FANCY', 'MOUSTACHE_MAGNUM'])
    list_hair_color = cycle(['AUBURN', 'BLACK', 'BLONDE', 'BLONDE_GOLDEN', 'BROWN', 'BROWN_DARK', 'PASTEL_PINK', 'PLATINUM', 'RED','SILVER_GRAY'])
    list_eyebrows_type = cycle(['NONE', 'ANGRY_NATURAL', 'ANGRY', 'DEFAULT_NATURAL', 'DEFAULT', 'FLAT_NATURAL', 'FROWN_NATURAL', 'RAISED_EXCITED_NATURAL', 'RAISED_EXCITED', 'SAD_CONCERNED_NATURAL', 'SAD_CONCERNED', 'UNIBROW_NATURAL', 'UP_DOWN_NATURAL', 'UP_DOWN'])
    list_clothing_color = cycle(['BLACK', 'BLUE_01', 'BLUE_02', 'BLUE_03', 'GRAY_01', 'HEATHER', 'PASTEL_BLUE', 'PASTEL_GREEN', 'PASTEL_ORANGE', 'PASTEL_YELLOW', 'PINK', 'RED', 'WHITE'])
    
    list_skin_colors = ['TANNED','YELLOW','PALE','LIGHT','BROWN','DARK_BROWN','BLACK']
    list_eye_types = ['CLOSED', 'CRY', 'DEFAULT', 'EYE_ROLL', 'HAPPY', 'HEART', 'SIDE', 'SQUINT', 'SURPRISED', 'WINK_WACKY', 'WINK', 'X_DIZZY']
    list_top_types = ['NONE', 'BIG_HAIR', 'BOB', 'BUN', 'CURLY', 'CURVY', 'DREADS', 'FRIDA', 'FRIZZLE', 'FRO_BAND', 'FRO', 'LONG_NOT_TOO_LONG', 'SHAGGY_MULLET', 'SHAGGY', 'SHAVED_SIDES', 'SHORT_CURLY', 'SHORT_DREADS_1', 'SHORT_DREADS_2', 'SHORT_FLAT', 'SHORT_ROUND', 'SHORT_WAVED', 'SIDES', 'STRAIGHT_1', 'STRAIGHT_2', 'STRAIGHT_STRAND']
    list_mouth_types = ['DEFAULT','CONCERNED','DISBELIEF','EATING','GRIMACE','SAD','SCREAM_OPEN','SERIOUS','SMILE','TONGUE','TWINKLE','VOMIT']
    list_accessories_types = ['NONE', 'KURT','ROUND','SUNGLASSES','WAYFARERS']
    list_clothe_types = ['BLAZER_SHIRT','BLAZER_SWEATER','COLLAR_SWEATER','GRAPHIC_SHIRT','HOODIE','OVERALL','SHIRT_CREW_NECK','SHIRT_SCOOP_NECK','SHIRT_V_NECK']
    list_facial_hair_types = ['NONE', 'BEARD_LIGHT', 'BEARD_MAGESTIC', 'BEARD_MEDIUM', 'MOUSTACHE_FANCY', 'MOUSTACHE_MAGNUM']
    list_hair_colors = ['AUBURN', 'BLACK', 'BLONDE', 'BLONDE_GOLDEN', 'BROWN', 'BROWN_DARK', 'PASTEL_PINK', 'PLATINUM', 'RED','SILVER_GRAY']
    list_eyebrows_types = ['NONE', 'ANGRY_NATURAL', 'ANGRY', 'DEFAULT_NATURAL', 'DEFAULT', 'FLAT_NATURAL', 'FROWN_NATURAL', 'RAISED_EXCITED_NATURAL', 'RAISED_EXCITED', 'SAD_CONCERNED_NATURAL', 'SAD_CONCERNED', 'UNIBROW_NATURAL', 'UP_DOWN_NATURAL', 'UP_DOWN']
    list_clothing_colors = ['BLACK', 'BLUE_01', 'BLUE_02', 'BLUE_03', 'GRAY_01', 'HEATHER', 'PASTEL_BLUE', 'PASTEL_GREEN', 'PASTEL_ORANGE', 'PASTEL_YELLOW', 'PINK', 'RED', 'WHITE']

    # Setting default avatar
    def change_skin(sk, ey, ha, mo, ac, sh, fh, hc, eb, cc):
        
        #Skin
        if sk == 1:
            skin = next(list_skin_color)
        if sk == -1:
            for i in range(len(list_skin_colors)-1):
                skin = next(list_skin_color)
        if sk == 0:
            for i in range(len(list_skin_colors)):
                skin = next(list_skin_color)
        if sk == 2:
            for i in range(random.randint(1, 9)):
                skin = next(list_skin_color)

        #Eyes
        if ey == 1:
            eye = next(list_eye_type)
        if ey == -1:
            for i in range(len(list_eye_types)-1):
                eye = next(list_eye_type)
        if ey == 0:
            for i in range(len(list_eye_types)):
                eye = next(list_eye_type)
        if ey == 2:
            for i in range(random.randint(1, 9)):
                eye = next(list_eye_type)
        
        #Hair
        if ha == 1:
            hair = next(list_top_type)
        if ha == -1:
            for i in range(len(list_top_types)-1):
                hair = next(list_top_type)
        if ha == 0:
            for i in range(len(list_top_types)):
                hair = next(list_top_type)
        if ha == 2:
            for i in range(random.randint(1, 9)):
                hair = next(list_top_type)
        #Mouth
        if mo == 1:
            mouth = next(list_mouth_type)
        if mo == -1:
            for i in range(len(list_mouth_types)-1):
                mouth = next(list_mouth_type)
        if mo == 0:
            for i in range(len(list_mouth_types)):
                mouth = next(list_mouth_type)
        if mo == 2:
            for i in range(random.randint(1, 9)):
                mouth = next(list_mouth_type)

        #Accessories
        if ac == 1:
            accessories = next(list_accessories_type)
        if ac == -1:
            for i in range(len(list_accessories_types)-1):
                accessories = next(list_accessories_type)
        if ac == 0:
            for i in range(len(list_accessories_types)):
                accessories = next(list_accessories_type)
        if ac == 2:
            for i in range(random.randint(1, 9)):
                accessories = next(list_accessories_type)

        #Clothes
        if sh == 1:
            clothes = next(list_clothe_type)
        if sh == -1:
            for i in range(len(list_clothe_types)-1):
                clothes = next(list_clothe_type)
        if sh == 0:
            for i in range(len(list_clothe_types)):
                clothes = next(list_clothe_type)
        if sh == 2:
            for i in range(random.randint(1, 9)):
                clothes = next(list_clothe_type)

        #Clothe Colors
        if cc == 1:
            clothecolor = next(list_clothing_color)
        if cc == -1:
            for i in range(len(list_clothing_colors)-1):
                clothecolor = next(list_clothing_color)
        if cc == 0:
            for i in range(len(list_clothing_colors)):
                clothecolor = next(list_clothing_color)
        if cc == 2:
            for i in range(random.randint(1, 9)):
                clothecolor = next(list_clothing_color)

        #Eyebrows
        if eb == 1:
            eye_brows = next(list_eyebrows_type)
        if eb == -1:
            for i in range(len(list_eyebrows_types)-1):
                eye_brows = next(list_eyebrows_type)
        if eb == 0:
            for i in range(len(list_eyebrows_types)):
                eye_brows = next(list_eyebrows_type)
        if eb == 2:
            for i in range(random.randint(1, 9)):
                eye_brows = next(list_eyebrows_type)

        #Hair Color
        if hc == 1:
            haircolor = next(list_hair_color)
        if hc == -1:
            for i in range(len(list_hair_colors)-1):
                haircolor = next(list_hair_color)
        if hc == 0:
            for i in range(len(list_hair_colors)):
                haircolor = next(list_hair_color)
        if hc == 2:
            for i in range(random.randint(1, 9)):
                haircolor = next(list_hair_color)

        #Facial Hair
        if fh == 1:
            facialhair = next(list_facial_hair_type)
        if fh == -1:
            for i in range(len(list_facial_hair_types)-1):
                facialhair = next(list_facial_hair_type)
        if fh == 0:
            for i in range(len(list_facial_hair_types)):
                facialhair = next(list_facial_hair_type)
        if fh == 2:
            for i in range(random.randint(1, 9)):
                facialhair = next(list_facial_hair_type)
        # Current saved avatar 
        my_avatar = pa.Avatar(
            skin_color=eval('pa.SkinColor.%s' % skin),
            eyes=eval('pa.EyeType.%s' % eye),
            top=eval('pa.HairType.%s' % hair),
            mouth=eval('pa.MouthType.%s' % mouth),
            accessory=eval('pa.AccessoryType.%s' % accessories),
            clothing=eval('pa.ClothingType.%s' % clothes),
            facial_hair=eval('pa.FacialHairType.%s' % facialhair),
            hair_color=eval('pa.HairColor.%s' % haircolor),
            eyebrows=eval('pa.EyebrowType.%s' % eye_brows),
            clothing_color=eval('pa.ClothingColor.%s' % clothecolor),
        )
        my_avatar.render("my_avatar.svg")
        pyvips.cache_set_max(0)
        image = pyvips.Image.new_from_file("my_avatar.svg", dpi=300)
        image.write_to_file("my_avatar.png")
    
#================== Frame 1 - Button creation code ======================================================#
    # Hair buttons & label
    hair_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    hair_bdr.place(x=49, y=242, height=42, width=77)
    hair_lbl = tk.Label(frame1, text="Hair", bg='white')
    hair_lbl.place(x=50, y=243, height=40, width=75)
    hair_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 1, 0, 0, 0, 0, 0, 0, 0), insert_img()])
    hair_right_btn.place(x=131, y=258, height=10, width=20)
    hair_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, -1, 0, 0, 0, 0, 0, 0, 0), insert_img()])
    hair_left_btn.place(x=24, y=258, height=10, width=20)

    # Hair Colour buttons & label
    hair_col_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    hair_col_bdr.place(x=49, y=293, height=42, width=77)
    hair_col_lbl = tk.Label(frame1, text="Hair Colour", bg='white')
    hair_col_lbl.place(x=50, y=294, height=40, width=75)
    hair_col_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 0, 1, 0, 0), insert_img()])
    hair_col_right_btn.place(x=131, y=309, height=10, width=20)
    hair_col_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 0, -1, 0, 0), insert_img()])
    hair_col_left_btn.place(x=24, y=309, height=10, width=20)

    # Skin buttons & label
    skin_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0) # creating background border
    skin_bdr.place(x=49, y=344, height=42, width=77) # placing border
    skin_lbl = tk.Label(frame1, text="Skin", bg='white') # creating skin label
    skin_lbl.place(x=50, y=345, height=40, width=75) # placing skin label
    skin_right_btn = tk.Button(frame1, command= lambda: [change_skin(1, 0, 0, 0, 0, 0, 0, 0, 0, 0), insert_img()]) # creating right button
    skin_right_btn.place(x=131, y=360, height=10, width=20) # placing right button
    skin_left_btn = tk.Button(frame1, command= lambda: [change_skin(-1, 0, 0, 0, 0, 0, 0, 0, 0, 0), insert_img()]) # creating left button
    skin_left_btn.place(x=24, y=360, height=10, width=20) # placing right button

    # Eyes buttons & label
    eyes_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    eyes_bdr.place(x=49, y=395, height=42, width=77)
    eyes_lbl = tk.Label(frame1, text="Eyes", bg='white')
    eyes_lbl.place(x=50, y=396, height=40, width=75)
    eyes_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 1, 0, 0, 0, 0, 0, 0, 0, 0), insert_img()])
    eyes_right_btn.place(x=131, y=411, height=10, width=20)
    eyes_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, -1, 0, 0, 0, 0, 0, 0, 0, 0), insert_img()])
    eyes_left_btn.place(x=24, y=411, height=10, width=20)

    # Eyebrows buttons & label
    brows_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    brows_bdr.place(x=49, y=446, height=42, width=77)
    brows_lbl = tk.Label(frame1, text="Eyebrows", bg='white')
    brows_lbl.place(x=50, y=447, height=40, width=75)
    brows_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 0, 0, 1, 0), insert_img()])
    brows_right_btn.place(x=131, y=462, height=10, width=20)
    brows_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 0, 0, -1, 0), insert_img()])
    brows_left_btn.place(x=24, y=462, height=10, width=20)

    # Shirt buttons & label
    shirt_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    shirt_bdr.place(x=274, y=242, height=42, width=77)
    shirt_lbl = tk.Label(frame1, text="Shirt", bg='white')
    shirt_lbl.place(x=275, y=243, height=40, width=75)
    shirt_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 1, 0, 0, 0, 0), insert_img()])
    shirt_right_btn.place(x=249, y=258, height=10, width=20)
    shirt_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, -1, 0, 0, 0, 0), insert_img()])
    shirt_left_btn.place(x=357, y=258, height=10, width=20)
    
    # Accessories buttons & label
    acc_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    acc_bdr.place(x=274, y=293, height=42, width=77)
    acc_lbl = tk.Label(frame1, text="Accessories", bg='white')
    acc_lbl.place(x=275, y=294, height=40, width=75)
    acc_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 1, 0, 0, 0, 0, 0), insert_img()])
    acc_right_btn.place(x=249, y=309, height=10, width=20)
    acc_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, -1, 0, 0, 0, 0, 0), insert_img()])
    acc_left_btn.place(x=356, y=309, height=10, width=20)

    # Mouth buttons & label
    mouth_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    mouth_bdr.place(x=274, y=344, height=42, width=77)
    mouth_lbl = tk.Label(frame1, text="Mouth", bg='white')
    mouth_lbl.place(x=275, y=345, height=40, width=75)
    mouth_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 1, 0, 0, 0, 0, 0, 0), insert_img()])
    mouth_right_btn.place(x=249, y=360, height=10, width=20)
    mouth_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, -1, 0, 0, 0, 0, 0, 0), insert_img()])
    mouth_left_btn.place(x=356, y=360, height=10, width=20)

    # Clothing Colours buttons & label
    nose_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    nose_bdr.place(x=274, y=395, height=42, width=77)
    nose_lbl = tk.Label(frame1, text="Clothing Colour", bg='white', wraplength=48, justify='center')
    nose_lbl.place(x=275, y=396, height=40, width=75)
    nose_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 0, 0, 0, 1), insert_img()])
    nose_right_btn.place(x=249, y=411, height=10, width=20)
    nose_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 0, 0, 0, -1), insert_img()])
    nose_left_btn.place(x=356, y=411, height=10, width=20)

    # Facial Hair buttons & label
    mouth_bdr = tk.Frame(frame1, highlightbackground = "black", highlightthickness = 2, bd=0)
    mouth_bdr.place(x=274, y=446, height=42, width=77)
    mouth_lbl = tk.Label(frame1, text="Facial Hair", bg='white')
    mouth_lbl.place(x=275, y=447, height=40, width=75)
    mouth_right_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, 1, 0, 0, 0), insert_img()])
    mouth_right_btn.place(x=249, y=462, height=10, width=20)
    mouth_left_btn = tk.Button(frame1, command= lambda: [change_skin(0, 0, 0, 0, 0, 0, -1, 0, 0, 0), insert_img()])
    mouth_left_btn.place(x=356, y=462, height=10, width=20)

    # Submition button
    submit_btn = tk.Button(frame1, text='Login',command=submit_button) 
    submit_btn.place(x=163, y=438, height=30, width=75)
    submit_btn.bind('<Return>', show_frame)
    
    # Random avatar button
    rand_btn = tk.Button(frame1, text="Randomise!", bg='white', command= lambda: [change_skin(2, 2, 2, 2, 2, 2, 2, 2, 2, 2), insert_img()])    
    rand_btn.place(x=163, y=300, height=50, width=75)
    
    #================== Frame 2 - Chat bot UI code =================================================#

    # chat window
    chat_window = Text(frame2, bd=1, bg="#84CBEE", width =50, height = 8, cursor="arrow", wrap=WORD, font= set_font)
    chat_window.place(x=6, y=72, height= 342, width= 388)
    chat_window.configure(state="disabled") # disables users for inputting directly into window
    
    hyperlink = HyperlinkManager(chat_window)

    # message window
    message_window = Text(frame2, bg="#84CBEE", width=30, cursor="arrow", wrap=WORD, font= set_font)
    message_window.place(x=6, y=426, height=66, width=388)

    #================== Frame 2 - Display Avatar =================================================#

    # top frame lefthand side SHORT
    top_frame = tk.Frame(frame2, highlightbackground = "black", highlightthickness = 2, bd=0)
    top_frame.place(x=6, y=6, width=388, height=65)
    # filler label righthand side LONG within filler_frame
    filler_label = Label(frame2, bg="#84CBEE")
    filler_label.place(x=7, y=7, width=386, height=63)

    # contains circle1 image within top_frame
    top_label = Label(frame2, bg="#84CBEE")
    top_label.place(x=7, y=7, width=64, height=63)

    # contains avatar image within top_label
    top_img_label = Label(frame2, bg="#84CBEE")
    top_img_label.place(x=160, y=14, width=50, height=50)
    
    # displaying frame 2 avatar within circle in top label
    def frame2_avatar():
        if exists('my_avatar.png'):
            photo1 = Image.open('my_avatar.png') # importing the image
        else:
            photo1 = Image.open('generic_avatar.png') # importing the image
        
        resize_img1 = photo1.resize((45, 45), Image.LANCZOS) # resizing 
        img1 = ImageTk.PhotoImage(resize_img1)
        top_img_label.image =img1 # saving reference of photo 
        top_img_label.place(x=180, y=19, height=40, width=40) # placing the image label
        top_img_label.configure(image=img1) # setting the label to the image
        
        circle = Image.open('circle.png')
        resize_circle = circle.resize((70,70), Image.LANCZOS)
        circle1 = ImageTk.PhotoImage(resize_circle)
        top_label.image = circle1
        top_label.place(x=168, y=7, height=63, width=63)
        top_label.configure(image=circle1)
    
    #================== Root Window buttons code =========================================================#

    # main menu bar 
    main_menu = Menu(root_window)

    # sub/dropdown menu 
    file_menu = Menu(root_window)
    file_menu.add_command(label="Clear Chat Window", command=lambda:[clear_chat_window(), chat_window_state()]) # un assigned menu
    file_menu.add_command(label="Log Out",command=lambda:[show_frame(frame1), clear_chat_window()])  # calls return frame1 function
    file_menu.add_command(label="Hush Mode", command=lambda:hush()) # calls hush function
    file_menu.add_command(label="About Us", command=lambda:aboutus.launchBrowser()) #calls a web about Yolia info
    file_menu.add_command(label="Help", command=lambda:help.launchHelp()) # instructions

    # main menu widgets 
    main_menu.add_cascade(label="Options", menu = file_menu)  # shows drop down button
    root_window.config(menu=main_menu) 

    frame2_avatar()
    show_frame(frame1)
    
    return root_window


class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

if __name__=="__main__":
    #window = create_window(lambda x: "Placeholder reply funtion")
    window = create_window(lambda x: "Placeholder reply funtion", lambda x:x)
    window.mainloop()