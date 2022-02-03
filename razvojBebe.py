from ast import keyword
from asyncio.windows_events import NULL
import datetime
from tkinter import font
from turtle import Screen, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#podaci=['0', 'testUser', '12345', '2022-01-13', '"2022-01-13 23:21:51.450349"', '']
#ime="Tea Teic"
def create_razvoj_window(podaci,ime):
    w_razvoj=tk.Tk()
   
    w_razvoj.title("Korisnik: "+ime +" - Razvoj Bebe")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    w_razvoj.iconphoto(False, slikaIcon)
    
    #povezi korisnika
    #velicina prozora
    window_width=400
    window_height=400

    #dohvati dimenzije ekrana

    screen_width=w_razvoj.winfo_screenwidth()
    screen_height=w_razvoj.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    w_razvoj.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    w_razvoj.resizable(0,0)
    
    #Layout
    w_razvoj.columnconfigure(0,weight=3)
    w_razvoj.columnconfigure(1,weight=3)
    w_razvoj.columnconfigure(2,weight=1)
    
    

    #dodaj gumbe
    layout(w_razvoj,podaci,ime)
    w_razvoj.mainloop()

def layout(container,podaci,ime):
    from tjedanTrudnoce import openMain
    frame=tk.Canvas(container)
    
    lbRazvoj=Label(container,text="RAZVOJ BEBE", font="FangSong 16 bold")
    lbRazvoj.grid(row=0,column=0,columnspan=2)    
    
    lbRazvoj=Label(container,text="Moj mjesec trudnoće - "+getMjesec(podaci[0]), font="FangSong 12")
    lbRazvoj.grid(row=1,column=0, stick=tk.N)
    
    txtRazvoj=Text(container,wrap=WORD, height=10, width=50)
    txtRazvoj.insert(1.0,getOpis(getMjesec(podaci[0])))
    txtRazvoj.configure(state='disabled')
    txtRazvoj.grid(row=2,column=0,sticky=tk.N)      
  
    btnDatumNazad=Button(frame,text="Nazad", command=lambda: openMain(podaci,ime,container))
    btnDatumNazad.grid(row=3,column=3,columnspan=2,sticky=tk.E)
    
    for widget in container.winfo_children():
            widget.grid(padx=0,pady=5)


def getMjesec(korisnikID):
    connect_db()
    cur=conn.cursor()
    query='select prosli_mjeseci('+korisnikID+');'
    cur.execute(query)
    prosliMjeseci=str(cur.fetchone())
    for character in "()',":
                prosliMjeseci=prosliMjeseci.replace(character,'')
    conn.commit()
    cur.close()
    
    return prosliMjeseci

def getOpis(mjeseci):
    connect_db()
    cur=conn.cursor()
    query='select opis from "Razvoj bebe" where "Mjesec trudnoce"='+mjeseci+';'
    cur.execute(query)
    string=str(cur.fetchone())
    conn.commit()
    cur.close()
    string=string[2:]
    string=string[:-3]
    string=string.replace("\\n","\n")
    print("Mjesec:"+mjeseci)
    
    return string
#if __name__ == "__main__":
    #create_razvoj_window(podaci,ime)    
