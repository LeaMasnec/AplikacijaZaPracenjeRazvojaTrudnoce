from ast import keyword
from asyncio.windows_events import NULL
import datetime
from tkinter import font
from turtle import Screen, end_fill, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#podaci=['0', 'testUser', '12345', '2022-01-13', '"2022-01-13 23:21:51.450349"', '']
#ime="Tea Teic"
def create_log_window(podaci,ime):
    w_log=tk.Tk()
   
    w_log.title("Korisnik: "+ime +" - moj login")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    w_log.iconphoto(False, slikaIcon)
    
    #povezi korisnika
    #velicina prozora
    window_width=400
    window_height=400

    #dohvati dimenzije ekrana

    screen_width=w_log.winfo_screenwidth()
    screen_height=w_log.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    w_log.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    w_log.resizable(0,0)
    
    #Layout
    w_log.columnconfigure(0,weight=3)
    w_log.columnconfigure(1,weight=3)
    w_log.columnconfigure(2,weight=1)
    
    

    #dodaj gumbe
    layout(w_log,podaci,ime)
    w_log.mainloop()

def layout(container,podaci,ime):
    from tjedanTrudnoce import openMain
    frame=tk.Canvas(container)
    
    scrollBar= Scrollbar(container,orient='vertical',command=frame.yview)
    frame.configure(yscrollcommand=scrollBar.set)
    
    
    lbRazvoj=Label(container,text="Moje prijave", font="FangSong 16 bold")
    lbRazvoj.grid(row=0,column=0,columnspan=2)    
    
    txtRazvoj=Text(container,wrap=WORD, height=10, width=50)
    txtRazvoj.insert(1.0,"Vremena prijave: \n")
    txtRazvoj.insert(END,"---------------- \n")
    
    getLog(txtRazvoj,podaci[0])
    txtRazvoj.configure(state='disabled')
    txtRazvoj.grid(row=1,column=0,sticky=tk.N)      
    scrollBar.grid(row=1,column=1)
    btnDatumNazad=Button(frame,text="Nazad", command=lambda: openMain(podaci,ime,container))
    btnDatumNazad.grid(row=2,column=1,columnspan=2,sticky=tk.E)
    
    for widget in container.winfo_children():
            widget.grid(padx=0,pady=5)


def getLog(txt,korisnikID):
    connect_db()
    cur=conn.cursor()
    query='select datum_logina from login_log where korisnickiracunid='+korisnikID+' order by datum_logina desc;'
    cur.execute(query)
    prosliMjeseci=cur.fetchall()
    for red in prosliMjeseci:
        txt.insert(END,"\n\n"+str(red[0])+"\n")
        txt.insert(END,"____________________________")        
    conn.commit()
    cur.close()
    return prosliMjeseci
    
    

#if __name__ == "__main__":
    create_log_window(podaci,ime)    
