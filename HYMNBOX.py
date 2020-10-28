import mysql.connector as msql

def write_Blob(data,filename):
    with open(filename,"wb") as file:
        file.write(data)

def read_Blob(name):
    con=msql.connect(host="65.19.141.67",database="rohandij_HYMNBOX",user="rohandij_hymnbox",password="hymnbox")
    cur=con.cursor()

    query="SELECT * FROM hymnbox WHERE  Name = %s"
    cur.execute(query,(name,))
    record = cur.fetchall()

    if record==[]:
        error_label.config(text="Sorry..\n Song is Unavailable")
        statusbar.config(text="")
    
    else:
        error_label.config(text="")


    for i in record:
        
        print("Name: ", i[0])
        song=i[1]
        name+=".mp3"
        write_Blob(song,name)
        print("Writing on disk")
    
    con.close()

import tkinter as tk
import pygame
import os
import tkinter.ttk as ttk
from mutagen.mp3 import MP3

root=tk.Tk()
root.title("HYMNBOX")
root.geometry("600x500")

photo=tk.PhotoImage(file="img\icon.png")
root.iconphoto(False,photo)

def submit():
    statusbar.config(text="Loading...")


    name=song_entry.get()

    song_entry.delete(0,"end")

    if name=="":
        name=listbox.get("active")

    global s
    s=name+".mp3"

    read_Blob(name)

    pygame.mixer.init()
    global f
    f=open(s)
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()

    song_mut=MP3(s)
    global duration
    duration=song_mut.info.length

    playtime()

    #Update slider position
    
    slider.config(to=duration,value=0)

    statusbar.config(text="Playing: {}".format(name.capitalize()))
    


def pause():
    pygame.mixer.music.pause()
    statusbar.config(text="Paused")

def unpause():
    pygame.mixer.music.unpause()
    statusbar.config(text="Unpaused")
    

def replay():
    pygame.mixer.music.rewind()
    statusbar.config(text="Replaying..")
    slider.config(value=0)
    

def stop():
    pygame.mixer.music.stop()
    f.close()
    if os.path.exists(s):
        os.remove(s)
    statusbar.config(text="Stopping..")
    
def playtime():
    global current_time
    current_time=pygame.mixer.music.get_pos()/1000

    slider.configure(value=current_time)
    slider.after(1000,playtime)

    if current_time < 0:
        stop()


canvas=tk.Canvas(root,bg="#464646")
canvas.place(relheight=1,relwidth=1)

label=tk.Label(canvas,text="HYMNBOX",bg="#464646",fg="#60C6DF", font="Times 20 bold")
label.place(relx=0.40,rely=0.01)

song_label=tk.Label(canvas,text="Enter Song:",fg="#60C6DF",bg="#464646",font="Times 13 italic bold")
song_label.place(relx=0.18,rely=0.16,relheight=0.042,relwidth=0.20)

song_entry=tk.Entry(canvas, width=30,font="Lucida 12 italic",bg="#B3B3B3")
song_entry.place(relx=0.35,rely=0.16,relheight=0.042,relwidth=0.4)

play_button=tk.Button(canvas,text="Play Song",fg="#285050",bg="#60C6DF",font="Times 12 italic",command=submit)
play_button.place(relx=0.44,rely=0.22,relheight=0.042,relwidth=0.12)

player_canvas=tk.Frame(canvas,bg="#212121")
player_canvas.place(rely=0.82,relheight=0.18,relwidth=1)

pause_icon=tk.PhotoImage(file="img\icon2.png")
pause_button=tk.Button(player_canvas,bg="#212121",image=pause_icon,borderwidth=0,command=pause)
pause_button.place(rely=0.50,relx=0.40,relheight=0.4,relwidth=0.055)

stop_icon=tk.PhotoImage(file="img\icon3.png")
stop_button=tk.Button(player_canvas,bg="#212121",image=stop_icon,borderwidth=0,command=stop)
stop_button.place(rely=0.50,relx=0.50,relheight=0.4,relwidth=0.055)

unpause_icon=tk.PhotoImage(file="img\icon1.png")
unpause_button=tk.Button(player_canvas,bg="#212121",image=unpause_icon,borderwidth=0,command=unpause)
unpause_button.place(rely=0.50,relx=0.30,relheight=0.4,relwidth=0.055)

replay_icon=tk.PhotoImage(file="img\icon4.png")
replay_button=tk.Button(player_canvas,bg="#212121",image=replay_icon,borderwidth=0,command=replay)
replay_button.place(rely=0.50,relx=0.60,relheight=0.4,relwidth=0.055)

slider=ttk.Scale(player_canvas,from_=0,orient="horizontal",value=0,command=playtime)
slider.place(rely=0.1,relx=0.24,relheight=0.3,relwidth=0.5)

s=ttk.Style()
s.configure("TScale",background="#212121")

statusbar=tk.Label(player_canvas,bg="#212121",fg="#60C6DF",font="Times 12 italic bold")
statusbar.place(relx=0.01,rely=0.35)

error_label=tk.Label(canvas,bg="#464646",fg="#60C6DF",font="Times 13 italic bold")
error_label.place(relx=0.38, rely=0.28)

frame=tk.Frame(canvas,bg="#464646")
frame.place(relx=0.20,rely=0.40,relwidth=0.6,relheight=0.4)

scrollbar=tk.Scrollbar(canvas,orient="vertical",bg="#B3B3B3")
scrollbar.place(relx=0.772,rely=0.402,relwidth=0.026,relheight=0.395)

listbox=tk.Listbox(frame,bg="#212121",fg="#60C6DF",font="Times 13 italic",selectbackground="#60C6DF",selectforeground="#212121",yscrollcommand=scrollbar.set)
listbox.place(relwidth=1,relheight=1)
scrollbar.config(command=listbox.yview)

con=msql.connect(host="65.19.141.67",database="rohandij_HYMNBOX",user="rohandij_hymnbox",password="hymnbox")
cur=con.cursor()

query="SELECT name FROM hymnbox ORDER BY name"
cur.execute(query)
songs = cur.fetchall()
for i in songs:
    name=i[0]
    listbox.insert("end",name)
con.close()

root.mainloop()