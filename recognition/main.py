import cv2
import numpy as np
import face_recognition


imgsteve = face_recognition.load_image_file('Photos/20190108002.jpg')
imgsteve = cv2.cvtColor(imgsteve, cv2.COLOR_BGR2RGB)
imgtest = face_recognition.load_image_file('Photos/20190108001.jpg')
imgtest = cv2.cvtColor(imgtest, cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgsteve)[0]
encodeSteve = face_recognition.face_encodings(imgsteve)[0]
cv2.rectangle(imgsteve, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

faceLocTest = face_recognition.face_locations(imgtest)[0]
encodeTest = face_recognition.face_encodings(imgtest)[0]
cv2.rectangle(imgtest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

results = face_recognition.compare_faces([encodeSteve], encodeTest)
faceDis = face_recognition.face_distance([encodeSteve], encodeTest)
cv2.putText(imgtest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


print(results)
print(faceDis)

cv2.imshow('steve', imgsteve)
cv2.imshow('test', imgtest)
cv2.waitKey(0)