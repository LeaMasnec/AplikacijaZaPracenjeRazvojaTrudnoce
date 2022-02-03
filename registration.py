from ast import keyword
from asyncio.windows_events import NULL
import datetime
from turtle import Screen, left, window_height, window_width
from venv import create
from connection import connect_db, close_db, conn
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry


def create_reg_window():
    w_reg=tk.Tk()
   
    w_reg.title("Registracija")
    slikaIcon=PhotoImage(file="Resursi/baby.png")
    w_reg.iconphoto(False, slikaIcon)
    
    #povezi korisnika
    #velicina prozora
    window_width=400
    window_height=300

    #dohvati dimenzije ekrana

    screen_width=w_reg.winfo_screenwidth()
    screen_height=w_reg.winfo_screenheight()

    #pronadi centar

    center_x=int(screen_width/2 - window_width /2)
    center_y=int(screen_height/2 - window_height /2)

    #pozicioniraj
    w_reg.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    w_reg.resizable(0,0)
    
    #Layout
    w_reg.columnconfigure(0,weight=4)
    w_reg.columnconfigure(1,weight=1)
    

    #dodaj gumbe
    layout(w_reg)
    w_reg.mainloop()

def layout(container):
    frame=tk.Frame(container)
        
    #korisnicko ime
    tk.Label(frame, text='Korisničko ime:').grid(column=0,row=0,sticky=tk.W)
    korime=tk.Entry(frame,width=45)
    korime.focus()
    korime.grid(column=1, row=0, sticky=tk.W)

    
    #lozinka
    tk.Label(frame, text='Lozinka:').grid(column=0,row=1,sticky=tk.W)
    lozinka=tk.Entry(frame,width=45,show="*")
    lozinka.grid(column=1, row=1, sticky=tk.W)
    tk.Label(frame, text='Potvrda lozinke:').grid(column=0,row=2,sticky=tk.W)
    lozinkaPT=tk.Entry(frame,width=45,show="*")
    lozinkaPT.grid(column=1, row=2, sticky=tk.W)
    
    tk.Label(frame, text='_________________________________').grid(column=0,row=3,sticky=tk.W)
    
    tk.Label(frame, text='Vaši podaci:').grid(column=0,row=4,sticky=tk.W)
    
    tk.Label(frame, text='Ime:').grid(column=0,row=5,sticky=tk.W)
    ime=tk.Entry(frame,width=45)
    ime.grid(column=1, row=5, sticky=tk.W)
    
    tk.Label(frame, text='Prezime:').grid(column=0,row=6,sticky=tk.W)
    prezime=tk.Entry(frame,width=45)
    prezime.grid(column=1, row=6, sticky=tk.W)
    
    tk.Label(frame, text='E-mail:').grid(column=0,row=7,sticky=tk.W)
    email=tk.Entry(frame,width=45)
    email.grid(column=1, row=7, sticky=tk.W)
    
    tk.Label(frame, text='Broj mobitela:').grid(column=0,row=8,sticky=tk.W)
    broj=tk.Entry(frame,width=45)
    broj.grid(column=1, row=8, sticky=tk.W)
    
    tk.Label(frame, text='Datum rodenja:').grid(column=0,row=9,sticky=tk.W)
    cal=DateEntry(frame,selectmode='day')
    cal.grid(row=9,column=1,padx=15, sticky=tk.W)
    
    tk.Label(frame,text='').grid(column=0,row=10)
    #login button
    tk.Button(frame,text='Nazad', command=lambda:openLogin(container)).grid(column=0,row=11)
    tk.Button(frame,text='Registracija', command=lambda: provjera()).grid(column=1,row=11)
    for widget in container.winfo_children():
            widget.grid(padx=0,pady=3)
    
    def mob_email_validation():
        special_ch = ['@', '.']
        msg = ''
        brojMobitela = broj.get()
        emailEntry=email.get()
        checkBroj=0
        if brojMobitela == '':
            msg = 'Unesite broj mobitela'
            checkBroj=1
        else:
                if not all(ch.isdigit() for ch in brojMobitela):
                        checkBroj=1
                        msg = 'Krivo unesen broj mobitela!'
                        
                else:
                    checkBroj=0
            
        if checkBroj==1:
            messagebox.showerror('Greška!', msg)
            return FALSE
        
        checkEmail=0
        if emailEntry =='':
            msg = 'Unesite e-mail'
            checkEmail=1
        else:
                if not any(ch in special_ch for ch in emailEntry):
                    msg = 'Uneseni e-mail je neispravan!'
                    checkEmail=1
                else:
                    checkEmail=0
        if checkEmail==1:
            messagebox.showerror("Greška!", msg)
            return FALSE
        else:
            return TRUE
            
  

    def validation(name_str, elm):
        msg = ''
        error=0
        if name_str == '':
            msg = f'{elm} je obavezno!'
            error=1
        else:
                if len(name_str) <= 2:
                    msg = f'{elm} je prekratko!'
                    error=1
                else:
                    if any(ch.isdigit() for ch in name_str):
                        msg = f'{elm} ne smije sadržavati brojeve!'
                        error=1
        if error==1:
            messagebox.showerror('Greška!', msg)
            return FALSE
        else:
            return TRUE
    
    def provjera():
        test=validation(ime.get(),"Ime")
        test=validation(prezime.get(),"Prezime")
        test=mob_email_validation()
        if korime.get()=='':
            test=FALSE
            messagebox.showerror("Greška!","Korisničko ime ne smije biti prazno")
        elif len(korime.get())<4:
            test=FALSE
            messagebox.showerror("Greška!","Korisničko ime je prekratko!")
        else:
            connect_db()
            cur=conn.cursor()
            query = 'Select * from "Korisnicki Racun";'
            cur.execute(query)
            korisnici = cur.fetchall()
            for korisnik in korisnici:
                if korisnik[1]==korime.get():
                    test=FALSE
                    messagebox.showerror("Greška!","Korisničko ime je zauzeto, odaberite novo korisničko ime!")
        date=cal.get_date()
        
        if lozinka.get()=='':
            messagebox.showerror("Greška!","Lozinka ne smije biti prazna")
            test=FALSE
        elif len(lozinka.get())<8:
            messagebox.showerror("Greška","Lozinka je premala!")
            test=FALSE
        elif lozinka.get()!=lozinkaPT.get():
            messagebox.showerror("Greška!","Unešene lozinke nisu jednake")
            test=FALSE
        if (date.today().year-cal.get_date().year) <10:
            messagebox.showerror("Greška!","Premladi ste da biste bili trudni!\n\nMolimo unesite ispravan datum!")
            test=FALSE
        if test==TRUE:
            UnesiNoviRacun()
        else:
            print("NAH")
        
    def UnesiNoviRacun():
        connect_db()
        cur=conn.cursor()
        query = 'INSERT INTO public."Korisnicki Racun"("idKorisnicki racun", "korisnicko ime", lozinka, "datum kreiranja racuna", "zadnja prijava", ime, prezime, "e-mail", "broj mobitela", "datum rodenja") '
        query=query+"VALUES (default,'"+korime.get()+"', '"+lozinka.get()+"', CURRENT_TIMESTAMP, NULL,'"+ime.get()+"', '"+prezime.get()+"', '"+email.get()+"', '"+broj.get()+"', '"+str(cal.get_date())+"');"
        cur.execute(query)
        conn.commit()
        cur.close()
        
        
def openLogin(root):
    from login import App
    root.destroy()
    root=App()
    root.mainloop()      

        
if __name__ == "__main__":
    create_reg_window()
        