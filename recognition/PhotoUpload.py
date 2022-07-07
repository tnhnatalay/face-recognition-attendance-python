import os
import sqlite3
import sys

import Login as Lg
import tkinter as tk
from tkinter import filedialog as fd
import cv2
from tkinter import messagebox

dosyayol = os.getcwd()
vt = sqlite3.connect("identifier.sqlite")
cursor = vt.cursor()
okulnum= Lg.new_okulnum.get()

Photo = tk.Tk()
Photo.title("FaceRecognition")
Photo.geometry("300x150")
Photo.configure(bg="#E6E6FA")
Photo.resizable(width=False,height=False)

Lg.LogoGetir()
FileDialog = tk.Button(Photo, text="Fotoğraf Ekle", bg="#C0C0C0",command=lambda : FotografEkle()).grid(padx=110, pady=10)

def FotografEkle():
    Foto = fd.askopenfilename()
    try:
        img = cv2.imread(Foto, 1)

        cv2.imwrite(dosyayol + "/Photos/" + okulnum + ".jpg", img)
        FotoYol = dosyayol + "\Photos"
        tk.messagebox.showinfo(title="Bilgi", message="Fotoğrafınız Sisteme Yüklendi.")
        sql = """UPDATE Ogrenciler
                 SET FotoYol = ? 
                 WHERE OkulNum = ?"""
        sql_values = (FotoYol, okulnum)
        cursor.execute(sql, sql_values)
        vt.commit()
        cv2.waitKey(0)
        Photo.destroy()

    except:
        tk.messagebox.showwarning(title="Hata", message="Fotoğraf Seçtiğinizden Emin Olunuz!")

def on_closing():
    if messagebox.askokcancel("Quit", "Kapatmak İstediğine Emin Misin ? :("):
        sys.exit()

Photo.protocol("WM_DELETE_WINDOW", on_closing)

Photo.mainloop()