import sqlite3
import string
import sys
import cv2
import numpy as np
import face_recognition
import os
import tkinter as tk
from tkinter import messagebox
import Section_Num as Sn
import datetime



Sec_Num = Sn.new_SecNum.get()
dersTarih = datetime.datetime.today()
bugun_format = datetime.datetime(dersTarih.year, dersTarih.month, dersTarih.day)
onceki_gun = datetime.datetime(dersTarih.year, dersTarih.month, dersTarih.day-1)

vt = sqlite3.connect("identifier.sqlite")
cursor = vt.cursor()

def AlinanCagir():
    sql = """SELECT Ogrenciler.OkulNum,Ogrenciler.OgrenciId,DersDetaylari.DersDetayId FROM AlinanDersler as al
    INNER JOIN Ogrenciler on al.OgrenciId = Ogrenciler.OgrenciId
    INNER JOIN DersDetaylari on al.DersDetayId = DersDetaylari.DersDetayId
    WHERE BolumNum={}""".format(f"'{Sec_Num}'")
    cursor.execute(sql)
    ds = cursor.fetchall()
    return ds

def yoklamayaYaz(ad):
    Num =""
    try:
        sql = """INSERT INTO Yoklama (OgrenciId, DersDetayId,Tarih) VALUES (?,?,?)"""
        ogrenci_Veri = AlinanCagir()
        for veri in ogrenci_Veri:
            if veri[0] == int(ad):
                dataset = yoklama_icKontrol(ad)
                if dataset != []:
                    for Tarih_Kontrol in dataset:
                        if Tarih_Kontrol != str(bugun_format):
                                cursor.execute(sql, (veri[1], veri[2], bugun_format))
                                vt.commit()
                else:
                    cursor.execute(sql, (veri[1], veri[2], bugun_format))
                    vt.commit()
    except:
        messagebox.showwarning(title="Hata")

def yoklama_icKontrol(ad):
    global ds
    try:
        sql = """SELECT Tarih FROM Yoklama 
        WHERE OgrenciId=? AND DersDetayId = ?"""
        ogrenci_Veri = AlinanCagir()
        for veri in ogrenci_Veri:
            if veri[0] == int(ad):
                sql_value = (veri[1], veri[2])
                cursor.execute(sql, sql_value)
                ds = cursor.fetchall()[-1]
        return ds
    except:
        return []

path = 'Photos'
images = []
classNames = []
myList = AlinanCagir()
Num = ""

for cl in myList:
    kaldir_Isaret = str(cl[0])
    for i in kaldir_Isaret:
        if i not in string.punctuation:
            Num += i
    getPhoto = f'{path}/{Num}.jpg'
    curImg = cv2.imread(getPhoto)
    images.append(curImg)
    classNames.append(os.path.splitext(Num)[0])
    Num = ""
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Tarama tamamlandı')


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    # img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            yoklamayaYaz(name)

    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
    k = cv2.waitKey(10) & 0xff  # Çıkış için Esc veya q tuşu
    if k == 27 or k == ord('q'):
        break
print("\n  Programdan çıkıyor")
