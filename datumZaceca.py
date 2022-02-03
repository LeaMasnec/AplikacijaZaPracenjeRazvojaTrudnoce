from ast import keyword
from asyncio.windows_events import NULL
from turtle import Screen, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import datetime


def create_zacece_window(podaci,ime,update):
    w_zacece=tk.Tk()
   
    w_zacece.title("Korisnik: "+ime +" - Datum začeća")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    w_zacece.iconphoto(False, slikaIcon)
    
    #povezi korisnika
    #velicina prozora
    window_width=400
    window_height=400

    #dohvati dimenzije ekrana

    screen_width=w_zacece.winfo_screenwidth()
    screen_height=w_zacece.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    w_zacece.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    w_zacece.resizable(0,0)
    
    #Layout
    w_zacece.columnconfigure(0,weight=4)
    w_zacece.columnconfigure(1,weight=1)
    

    #dodaj gumbe
    layout(w_zacece,podaci,ime,update)
    w_zacece.mainloop()

def layout(container,podaci,ime,update):
    if update==FALSE:
        from tjedanTrudnoce import create_ttrudnoce_window
        
        currentDatetime=datetime.datetime.now()
        date=currentDatetime.date()
        label=Label(container,text="Odabrani datum zaceca:")
        label.pack(pady=10)
        cal=Calendar(container,selectmode='day',year=date.year,month=date.month,day=date.day )
        cal.pack(pady=10)
        def spremiDatumZaceca():
            datum=cal.get_date()
            connect_db()
            query='insert into "Tjedan trudnoce" Values ' + "(default,null,"+podaci[0]+",'"+datum+"');"
            cur=conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()
            container.destroy()
            create_ttrudnoce_window(podaci,ime)
        def get_date():
            label.config(text="Odabrani datum zaceca: "+cal.get_date())
        button= Button(container, text= "Odaberite datum zaceca", command= spremiDatumZaceca)
        button.pack(pady=10)
        buttonBack= Button(container, text= "nazad", command= lambda: returnBack(update,container,podaci,ime))
        buttonBack.pack(pady=20)
        
    else:
        from tjedanTrudnoce import create_ttrudnoce_window
        
        currentDatetime=datetime.datetime.now()
        date=currentDatetime.date()
        label=Label(container,text="Odabrani datum zaceca:")
        label.pack(pady=10)
        cal=Calendar(container,selectmode='day',year=date.year,month=date.month,day=date.day )
        cal.pack(pady=10)
        def spremiDatumZaceca():
            datum=cal.get_date()
            connect_db()
            query='update "Tjedan trudnoce"' +"set datum_zaceca='"+datum+"' where korisnickiracunid="+podaci[0]+";"
            cur=conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()
            container.destroy()
            create_ttrudnoce_window(podaci,ime)
        def get_date():
            label.config(text="Odabrani datum zaceca: "+cal.get_date())
        button= Button(container, text= "Odaberite datum zaceca", command= spremiDatumZaceca)
        button.pack(pady=10)
        buttonBack= Button(container, text= "nazad", command= lambda: returnBack(update,container,podaci,ime))
        buttonBack.pack(pady=20)
       
def returnBack(update,container,podaci,ime):
        from main import create_main_window
        from tjedanTrudnoce import create_ttrudnoce_window
        if update==FALSE:
            container.destroy()
            create_main_window(ime,podaci)
        else:
            container.destroy()
            create_ttrudnoce_window(podaci,ime)

    