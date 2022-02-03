from ast import keyword
from turtle import Screen, window_height, window_width
from connection import connect_db, close_db, conn
import tkinter as tk
from main import create_main_window
from tkinter import *
from tkinter import messagebox



class App(tk.Tk):
    def __init__(self):
        
        super().__init__()
        self.title("Prijava")
        #velicina prozora
        window_width=400
        window_height=200
        self.bind('<Enter>',)
        #dohvati dimenzije ekrana
        slikaIcon=PhotoImage(file="Resursi/baby.png")
        self.iconphoto(False, slikaIcon)
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()

        #pronadi centar

        center_x=int(screen_width/2 - window_width /2)
        center_y=int(screen_height/2 - window_height /2)

        #pozicioniraj
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(0,0)
        #nema min max
        self.attributes('-toolwindow',True)
        #Layout
        self.columnconfigure(0,weight=4)
        self.columnconfigure(1,weight=1)
        
        input_frame=create_input_frame(self)
        input_frame.place(relx=.5, rely=.5, anchor="center")
    def destroy(self) -> None:
        return super().destroy()
#funkcije
#Funkcija za definiranje inputa
def create_input_frame(container):
            
        frame=tk.Frame(container)
        
        #layout grida
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)
        
        #korisnicko ime
        tk.Label(frame, text='Korisničko ime:').grid(column=0,row=0,sticky=tk.W)
        korime=tk.Entry(frame,width=45)
        korime.focus()
        korime.grid(column=1, row=0, sticky=tk.W)
    
        
        #lozinka
        tk.Label(frame, text='Lozinka:').grid(column=0,row=1,sticky=tk.W)
        lozinka=tk.Entry(frame,width=45,show="*")
        lozinka.grid(column=1, row=1, sticky=tk.W)
        
        #login button
        tk.Button(frame,text='Prijava', command=lambda: [check_login_info(korime.get(),lozinka.get(),container), lozinka.delete(0, END), korime.delete(0,END)]).grid(column=1,row=2)
        
        tk.Button(frame,text='Registracija', command= lambda: openRegister(container)).grid(column=0,row=2)
        
        for widget in frame.winfo_children():
            widget.grid(padx=0,pady=3)
            
        return frame
        





def check_login_info(user,password,container):
        #Baza
        connect_db()
        
        cur=conn.cursor()
        query = "select login_korisnika ('"+user+"','"+password+"');"
        cur.execute(query)
        if(cur.rowcount!=0):
            string=str(cur.fetchone())
            for character in "()'":
                string=string.replace(character,'')
            print(string)
            podaci=string.split(',')
            print(podaci)
            ###Dohvati joj ime 
            dohvatiImeQuery="select dohvati_ime_korisnice('"+podaci[0]+"');"
            cur.execute(dohvatiImeQuery)
            nazivKorisnika=str(cur.fetchone())
            for character in "()',":
                nazivKorisnika=nazivKorisnika.replace(character,'')
            messagebox.showinfo("Uspješna prijava!","Dobrodošla "+nazivKorisnika+"!")
            conn.commit()
            query='update "Korisnicki Racun" set "zadnja prijava" = CURRENT_TIMESTAMP where "idKorisnicki racun"='+podaci[0]+';'
            cur.execute(query)
            conn.commit()
            cur.close()
            container.destroy()
            create_main_window(nazivKorisnika,podaci)
            
        else:
            messagebox.showerror("Neuspješna prijava!","Korisnik nije pronađen!")
            conn.commit()
            cur.close()
    
        
def openRegister(container):
    from registration import create_reg_window
    container.destroy()
    create_reg_window()


    
    
if __name__ == "__main__":
    root=App()
    root.mainloop()
