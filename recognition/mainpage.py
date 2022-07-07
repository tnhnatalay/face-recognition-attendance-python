import os
import tkinter as tk

mainpage = tk.Tk()
mainpage.title("Main Page")
mainpage.geometry("250x220")
mainpage.configure(bg="#E6E6FA")

OgrenciPanel = tk.Button(mainpage, text="Öğrenci Giriş", bg="#C0C0C0", width=31, height=5,command=lambda : ogrenciPanelGit()).grid(padx=10, pady=10)

OgretmenPanel = tk.Button(mainpage, text="Akademisyen Giriş", bg="#C0C0C0", width=31, height=5,command=lambda :ogretmenPanelGit()).grid(padx=10, pady=10)

def ogrenciPanelGit():
    mainpage.destroy()
    os.system("python FaceControl.py")


def ogretmenPanelGit():
    mainpage.destroy()
    os.system("python Report.py")

mainpage.mainloop()