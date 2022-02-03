from ast import keyword
from asyncio.windows_events import NULL
from cgitb import text
import datetime
from msilib.schema import ComboBox
from textwrap import fill
from tkinter.ttk import Combobox
from tracemalloc import start
from turtle import Screen, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
import tkinter as tk
from tkinter import *
from tkinter import messagebox


#podaci=['0', 'testUser', '12345', '2022-01-13', '"2022-01-13 23:21:51.450349"', '']
#ime="Tea Teic"
def create_biljeska_window(podaci,ime):
    w_biljeska=tk.Tk()
   
    w_biljeska.title("Korisnik: "+ime +" - Moje bilješke")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    w_biljeska.iconphoto(False, slikaIcon)
    
    
    #povezi korisnika
    #velicina prozora
    window_width=500
    window_height=700

    #dohvati dimenzije ekrana

    screen_width=w_biljeska.winfo_screenwidth()
    screen_height=w_biljeska.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    w_biljeska.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    w_biljeska.resizable(0,0)
    
    #Layout
    w_biljeska.columnconfigure(0,weight=2)
    w_biljeska.columnconfigure(1,weight=0)
    w_biljeska.columnconfigure(2,weight=0)

    #dodaj gumbe
    layout(w_biljeska,podaci,ime)
    w_biljeska.mainloop()

def layout(container,podaci,ime):
    from razvojBebe import getMjesec
    frame=tk.Canvas(container)
    
    scrollBar= Scrollbar(container,orient='vertical',command=frame.yview)
    frame.configure(yscrollcommand=scrollBar.set)

    lbRazvoj=Label(container,text="Moje biljeske", font="FangSong 16 bold")
    lbRazvoj.grid(row=0,column=0,columnspan=2)    
    
    lbRazvoj=Label(container,text="Moj mjesec trudnoće - "+getMjesec(podaci[0]), font="FangSong 12")
    lbRazvoj.grid(row=1,column=0, stick=tk.W)
     
    lbOdaberi=Label(container,text="Odabrani mjesec trudnoće: ",font="FangSong 12")
    lbOdaberi.grid(row=2,column=0, stick=tk.W)
    odabraniMjesec=[0,1,2,3,4,5,6,7,8,9]
    cmbMjesec=Combobox(container,values=odabraniMjesec, width=2)
    cmbMjesec.current(0)
    cmbMjesec['state']='readonly'
    cmbMjesec.grid(row=2,column=1,sticky=tk.W)
    layout.index=0

     

    cmbMjesec.bind('<<ComboboxSelected>>', lambda event, obj=cmbMjesec:month_changed(event,layout.index))
    txtRazvoj=Text(container,wrap=WORD, height=30, width=55,yscrollcommand=scrollBar.set)
    txtRazvoj.insert(1.0,dohvatiNultiText(podaci[0]))
    
    scrollBar.grid(row=3,column=2, sticky='ns')
    frame.config(scrollregion=frame.bbox("all"))
    scrollBar.configure(command=txtRazvoj.yview)
    txtRazvoj.grid(row=3,column=0,sticky=tk.N,columnspan=2)      
    
    tk.Label(frame,text='').grid(column=1,row=4,sticky='n')
    tk.Label(frame,text='').grid(column=1,row=5,sticky='n')
    
    btnDatumNazad=Button(container,text="Nazad", command=lambda: zatvoriProzor(container,ime,podaci))
    btnDatumNazad.grid(row=5,column=1,sticky='ew')
    
    btnSave=Button(container,text="Spremi promjene", command=lambda: [spremiTekst(podaci[0],str(layout.index))])
    btnSave.grid(row=5,column=0)
    
    for widget in container.winfo_children():
            widget.grid(padx=0,pady=5)

    def month_changed(event, index):
        value=cmbMjesec.get() 
        provjera=provjeriText(podaci[0])
        provjera2=txtRazvoj.get(1.0,"end - 1 chars")
        
        print("Provjera tekst:"+provjera)
        print("Dohvacen tekst:"+provjera2)
        
        if int(value)!=index:
            if provjera!=provjera2:
                res = messagebox.askquestion('Potvrdite spremanje', 'Želite li spremiti promjene?')
                if res=='yes':
                    spremiTekst(podaci[0],str(layout.index))
                promijeniIndex(value)
                dohvatiText(podaci)
            else:
                promijeniIndex(value)
                dohvatiText(podaci)
            
        
    def promijeniIndex(novaVrijednost):
        layout.index=int(novaVrijednost)
        
    def dohvatiText(podaci):
        connect_db()
        cur=conn.cursor()
        query = 'select biljeska from biljeska where "KorisnickiRacunID"='+podaci[0]+"AND mjesec="+cmbMjesec.get()+";"
        cur.execute(query)
        if(cur.rowcount!=0):
            string=str(cur.fetchone())
            string=string[2:]
            string=string[:-3]
            for character in "\n":
                string=string.replace("\\n","\n")
            postaviString(string)
            
    def provjeriText(korisnik):
        connect_db()
        cur=conn.cursor()
        query = 'select biljeska from biljeska where "KorisnickiRacunID"='+podaci[0]+"AND mjesec="+str(layout.index)+";"
        cur.execute(query)
        if(cur.rowcount!=0):
            string=str(cur.fetchone())
            string=string[2:]
            string=string[:-3]
            string=string.replace("\\n","\n")
        return string
            
    def postaviString(string):
        txtRazvoj.delete(1.0,END)
        txtRazvoj.insert(1.0,string)
        
    def spremiTekst(korisnikID,mjesec):
        try:
            string=txtRazvoj.get(1.0,END)
            cur=conn.cursor()
            query="Update biljeska set biljeska='"+string+"'" + ' where "KorisnickiRacunID"='+korisnikID+' AND mjesec='+mjesec+';'
            cur.execute(query)
            conn.commit()
            query="Update biljeska set zadnji_update=CURRENT_TIMESTAMP " + ' where "KorisnickiRacunID"='+korisnikID+' AND mjesec='+mjesec+';'
            cur.execute(query)
            conn.commit()
            cur.close()
            messagebox.showinfo("Obavijest","Uspiješno ste spremili bilješku!")
        except Exception as error:
            messagebox.showerror("Greška!","Error message:\n"+str(error))
        
def zatvoriProzor(container,ime,podaci):
    from main import create_main_window
    container.destroy()
    create_main_window(ime,podaci)   
     
def dohvatiNultiText(korisnik):
    connect_db()
    cur=conn.cursor()
    query = 'select biljeska from biljeska where "KorisnickiRacunID"='+korisnik+"AND mjesec=0;"
    cur.execute(query)
    if(cur.rowcount!=0):
        string=str(cur.fetchone())
        string=string[2:]
        string=string[:-3]
        string=string.replace("\\n","\n")
        return string

  
