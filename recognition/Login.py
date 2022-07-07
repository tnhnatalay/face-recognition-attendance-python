import os
import sqlite3
import sys
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox

vt = sqlite3.connect("identifier.sqlite")
cursor = vt.cursor()
def LogoGetir():
    filepath = os.path.abspath('PiriReisUniversitesiLogo.png')
    image1 = Image.open(filepath)
    test = ImageTk.PhotoImage(image1)

    label1 = tk.Label(image=test,bg="#E6E6FA")
    label1.image = test
    label1.grid()


login = tk.Tk()
login.title("FaceRecognition")
login.geometry("350x350")
login.configure(bg="#E6E6FA")
login.resizable(width=False,height=False)

new_okulnum = tk.StringVar()
new_sifre = tk.StringVar()

LogoGetir()
OkulNum = tk.Label(login, bg="#E6E6FA", text="Okul Numarası").grid(padx=110, pady=10)
kg1 = tk.Entry(login, textvariable=new_okulnum).grid(padx=110, pady=10)

sifregiris = tk.Label(login, bg="#E6E6FA", text="Şifre").grid(padx=110, pady=10)
kg2 = tk.Entry(login, show="*", textvariable=new_sifre).grid(padx=110, pady=10)

girisbuton = tk.Button(login, text="Giriş Yap", bg="#C0C0C0",command=lambda :KontrolSifre()).grid(padx=110, pady=10)

def KontrolSifre():
    GetNumber = new_okulnum.get()
    GetPass = new_sifre.get()
    try:
        sql = """SELECT OkulNum,Sifre FROM Ogrenciler WHERE OkulNum={}""".format(GetNumber)
        cursor.execute(sql)
        ds = cursor.fetchone()

        DsNum = ds[0]
        DsSifre = ds[1]

        if int(GetNumber) == DsNum:
            if GetPass == DsSifre:
                tk.messagebox.showinfo(title="Bilgi", message="Giriş Gerçekleştirildi.")
                login.destroy()
            else:
                tk.messagebox.showwarning(title="Hata", message="Şifre Hatalı Tekrar Deneyiniz.")
        else:
            tk.messagebox.showwarning(title="Hata", message="Okul Numaranız Hatalı Tekrar Deneyiniz.")
    except:
        tk.messagebox.showwarning(title="Hata",message="Alanları Kontrol Ediniz. Bilgilerinizi Doğru Giriniz.")

def on_closing():
    if messagebox.askokcancel("Quit", "Kapatmak İstediğine Emin Misin ? :("):
        sys.exit()

login.protocol("WM_DELETE_WINDOW", on_closing)

login.mainloop()