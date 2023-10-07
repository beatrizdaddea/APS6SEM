import cv2
import face_recognition
import numpy as np

imagemID1 = face_recognition.load_image_file("Beatriz.jpg")
codificacaoID1 = face_recognition.face_encodings(imagemID1)[0]

imagemID2 = face_recognition.load_image_file("Mateus.jpg")
codificacaoID2 = face_recognition.face_encodings(imagemID2)[0]

imagemID3 = face_recognition.load_image_file("Rafael.jpg")
codificacaoID3 = face_recognition.face_encodings(imagemID3)[0]

camera = cv2.VideoCapture(0)

cv2.namedWindow("Sistema de Seguranca", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Sistema de Seguranca", 800, 600)  

codFacesConhecidas = [
    codificacaoID1,
    codificacaoID2,
    codificacaoID3
]
nomeFacesConhecidas = [
    "Beatriz",
    "Mateus",
    "Rafael"
]

codificacoes = []

while True:
    ret, frame = camera.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    posicaoDoRosto = face_recognition.face_locations(rgb_small_frame)
    if posicaoDoRosto:
        codificacoes = face_recognition.face_encodings(rgb_small_frame, posicaoDoRosto)
        
        nomeFaces = []
        for codificacao in codificacoes:
            nivelDeAcesso = None

            if face_recognition.compare_faces([codificacaoID1], codificacao)[0]:
                nivelDeAcesso = "Nivel 1"
                        
            elif face_recognition.compare_faces([codificacaoID2], codificacao)[0]:
                nivelDeAcesso = "Nivel 2"

            elif face_recognition.compare_faces([codificacaoID3], codificacao)[0]:
                nivelDeAcesso = "Nivel 3"
            
            comparacao = face_recognition.compare_faces(codFacesConhecidas, codificacao)
            nome = "Unknown"
            distanciaDoRosto = face_recognition.face_distance(codFacesConhecidas, codificacao)
            index = np.argmin(distanciaDoRosto)
            if comparacao[index]:
                nome = nomeFacesConhecidas[index] + " - " + nivelDeAcesso
            nomeFaces.append(nome)

        
    for (top, right, bottom, left), name in zip(posicaoDoRosto, nomeFaces):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom), (right, bottom + 35), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, bottom + 30), font, 0.6, (255, 255, 255), 1)

    cv2.imshow("Sistema de Seguranca", frame)

    if cv2.waitKey(5) == 27:
        break

camera.release()
cv2.destroyAllWindows()