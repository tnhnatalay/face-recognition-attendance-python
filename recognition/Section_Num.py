import os
import sqlite3
import string
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

    label1 = tk.Label(image=test, bg="#E6E6FA")
    label1.image = test
    label1.grid()

attendance = tk.Tk()
attendance.title("Attendance")
attendance.geometry("350x350")
attendance.configure(bg="#E6E6FA")
attendance.resizable(width=False, height=False)

new_SecNum = tk.StringVar()

LogoGetir()
SecNum = tk.Label(attendance, bg="#E6E6FA", text="Ders Kodu").grid(padx=110, pady=10)
kg1 = tk.Entry(attendance, textvariable=new_SecNum).grid(padx=110, pady=10)

girisbuton = tk.Button(attendance, text="Giriş Yap", bg="#C0C0C0",command=lambda : Kontrol_SecNum()).grid(padx=110, pady=10)


def Kontrol_SecNum():
    GetNumber = new_SecNum.get()
    try:
        sql = """SELECT BolumNum FROM DersDetaylari WHERE BolumNum={}""".format(f"'{GetNumber}'")
        cursor.execute(sql)
        ds = cursor.fetchall()

        degisenA=""
        kaldir_Isaret = str(ds[0])
        for i in kaldir_Isaret:
            if i not in string.punctuation:
                degisenA += i

        if GetNumber == degisenA:
                tk.messagebox.showinfo(title="Bilgi", message="Giriş Gerçekleştirildi.")
                attendance.destroy()
        else:
            tk.messagebox.showwarning(title="Hata", message="Şifre Hatalı Tekrar Deneyiniz.")
    except:
        tk.messagebox.showwarning(title="Hata", message="Alanları Kontrol Ediniz. Bilgilerinizi Doğru Giriniz.")

def on_closing():
    if messagebox.askokcancel("Quit", "Kapatmak İstediğine Emin Misin ? :("):
        sys.exit()

attendance.protocol("WM_DELETE_WINDOW", on_closing)

attendance.mainloop()