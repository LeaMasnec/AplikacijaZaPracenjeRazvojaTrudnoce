from ast import keyword
from asyncio.windows_events import NULL
import datetime
from turtle import Screen, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#podaci=['0', 'testUser', '12345', '2022-01-13', '"2022-01-13 23:21:51.450349"', '']
#ime="Tea Teic"
def create_ttrudnoce_window(podaci,ime):
    w_ttrudnoce=tk.Tk()
   
    w_ttrudnoce.title("Korisnik: "+ime +" - Tjedan trudnoce")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    w_ttrudnoce.iconphoto(False, slikaIcon)
    
    #povezi korisnika
    #velicina prozora
    window_width=400
    window_height=170

    #dohvati dimenzije ekrana

    screen_width=w_ttrudnoce.winfo_screenwidth()
    screen_height=w_ttrudnoce.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    w_ttrudnoce.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    w_ttrudnoce.resizable(0,0)
    
    #Layout
    w_ttrudnoce.columnconfigure(0,weight=4)
    w_ttrudnoce.columnconfigure(1,weight=1)
    

    #dodaj gumbe
    layout(w_ttrudnoce,podaci,ime)
    w_ttrudnoce.mainloop()

def layout(container,podaci,ime):
    
    frame=tk.Frame(container)
    
    labelTitle=Label(frame,text="TJEDAN TRUDNOCE", font="FangSong 16 bold")
    labelTitle.grid(column=1,row=0, columnspan=2)
    
    tk.Label(frame,text='').grid(column=1,row=1)
    label=Label(frame,text="Moj tjedan trudnoće: "+ get_tjedan_trudnoce(podaci[0]))
    label.grid(column=1,row=2,sticky=tk.W)
    
    labelZacece=Label(frame,text="Datum začeća: "+ get_datum_zaceca(podaci[0]))
    labelZacece.grid(column=1,row=3,sticky=tk.W)
    
    lbDatum=Label(frame,text="Predviđeni datum rođenja: "+ get_datum_rodenja(podaci[0]))
    lbDatum.grid(column=1,row=4,sticky=tk.W)
    
    btnDatumZaceca=Button(frame,text="Promijeni Datum zaceca", command=lambda: promijeniZacece(podaci,ime,container))
    btnDatumZaceca.grid(column=1,row=5,sticky=tk.W)
    
    btnDatumNazad=Button(frame,text="Nazad", command=lambda: openMain(podaci,ime,container))
    btnDatumNazad.grid(column=2, row=6,sticky=tk.W)
    
    for widget in container.winfo_children():
            widget.grid(padx=0,pady=3)

def get_tjedan_trudnoce(korisnikID):
        connect_db()
        cur=conn.cursor()
        query = 'select "Broj tjedna" from "Tjedan trudnoce" where korisnickiracunid='+korisnikID+';'
        cur.execute(query)
        brojTjedna=str(cur.fetchone())
        for character in "()',":
                brojTjedna=brojTjedna.replace(character,'')
        conn.commit()
        cur.close()
        
        return brojTjedna
    
def get_datum_zaceca(korisnikID):
    connect_db()
    cur=conn.cursor()
    query = 'select datum_zaceca from "Tjedan trudnoce" where korisnickiracunid='+korisnikID+';'
    cur.execute(query)
    datumZaceca=cur.fetchone()
    conn.commit()
    cur.close()
    return datumZaceca[0].strftime('%d.%m.%Y')

def get_datum_rodenja(korisnikID):
        connect_db()
        cur=conn.cursor()
        query = 'select datum_zaceca from "Tjedan trudnoce" where korisnickiracunid='+korisnikID+';'
        cur.execute(query)
        datumZaceca=cur.fetchone()
        datum=datumZaceca[0]
        print("Zacece datum: "+str(datum))
        queryRodenje="select datum_rodenja('"+str(datum)+"');"
        cur.execute(queryRodenje)
        predvideniDatum=cur.fetchone()
        
        print("Predvideni datum: "+str(predvideniDatum[0]))
        conn.commit()
        cur.close()
        datumRodenja=predvideniDatum[0].strftime('%d.%m.%Y')
        return datumRodenja
    
def promijeniZacece(podaci,ime,container):
    from datumZaceca import create_zacece_window
    container.destroy()
    create_zacece_window(podaci,ime,TRUE)
def openMain(podaci,ime,container):
    from main import create_main_window
    container.destroy()
    create_main_window(ime,podaci)
#if __name__ == "__main__":
    #create_ttrudnoce_window(podaci,ime)    
