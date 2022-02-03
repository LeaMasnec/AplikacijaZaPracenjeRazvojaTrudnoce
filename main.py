from ast import keyword
from asyncio.windows_events import NULL
from turtle import Screen, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
from datumZaceca import create_zacece_window
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tjedanTrudnoce import create_ttrudnoce_window

#podaci=['0', 'testUser', '12345', '2022-01-13', '"2022-01-13 23:21:51.450349"', '']
#ime="Tea Teic"
def create_main_window(naziv,podaci):
    main=tk.Tk()
    ime=naziv
    main.title("Korisnik: "+ime +" - Glavna forma")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    main.iconphoto(False, slikaIcon)
    
    #povezi korisnika
    korisnik=podaci
    #velicina prozora
    window_width=400
    window_height=205

    #dohvati dimenzije ekrana

    screen_width=main.winfo_screenwidth()
    screen_height=main.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    main.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    main.resizable(0,0)
    
    #Layout
    main.columnconfigure(0,weight=4)
    main.columnconfigure(1,weight=1)
    
    #dodaj gumbe
    buttons(main,korisnik,ime,main)
    main.mainloop()

def buttons(container,podaci,ime,main):
    from razvojBebe import create_razvoj_window
    Button(
    container,
    text='Moj tjedan trudnoće',
    command=lambda: [openTjedan(podaci,ime,main)],
    bg='#ac81b6',
    fg='#fce9dc',
    font='FangSong 16 bold'
            ).pack(fill=BOTH)
        
    Button(
    container,
    text='Razvoj bebe',
    command=lambda: [container.destroy(), create_razvoj_window(podaci,ime)],
    bg='#ac81b6',
    fg='#fce9dc',
    font='FangSong 16 bold'
            ).pack(fill=BOTH)
        
    Button(
    container,
    text='Moje bilješke',
    command=lambda: openBiljeska(container,podaci,ime),
    bg='#ac81b6',
    fg='#fce9dc',
    font='FangSong 16 bold'
            ).pack(fill=BOTH)
    
    Button(
    container,
    text='Moje prijave',
    command=lambda: openLog(container,podaci,ime),
    bg='#ac81b6',
    fg='#fce9dc',
    font='FangSong 16 bold'
            ).pack(fill=BOTH)
        
    Button( 
    container,
    text='Odjavi',
    command=lambda: openLogin(container),
    bg='#fce9dc',
    fg='#ac81b6',
    font='FangSong 16 bold'
            ).pack(fill=BOTH)
        
def openTjedan(podaci,ime,main):
        connect_db()
        query='select * from "Tjedan trudnoce" where korisnickiracunid='+podaci[0]+';'
        cur=conn.cursor()
        cur.execute(query)
        if(cur.rowcount!=0):
                print("Postoji")
                conn.commit()
                cur.close()
                main.destroy()
                create_ttrudnoce_window(podaci,ime)
        else:
                conn.commit()
                cur.close()
                main.destroy()
                create_zacece_window(podaci,ime,FALSE)

def openLogin(container):
        from login import App
        container.destroy()
        root=App()
        root.mainloop()   
        
def openBiljeska(container,podaci,ime):
        from biljeske import create_biljeska_window
        container.destroy()
        create_biljeska_window(podaci,ime)

def openLog(container,podaci,ime):
        from log import create_log_window
        container.destroy()
        create_log_window(podaci,ime)