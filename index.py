import cv2
import face_recognition

# Carregue as imagens de referência e codifique-as
imagem_referencia_nivel1 = face_recognition.load_image_file("px-woman-smilings.jpg")
codificacao_referencia_nivel1 = face_recognition.face_encodings(imagem_referencia_nivel1)[0]

imagem_referencia_nivel2 = face_recognition.load_image_file("px-woman-smilings.jpg")
codificacao_referencia_nivel2 = face_recognition.face_encodings(imagem_referencia_nivel2)[0]

imagem_referencia_nivel3 = face_recognition.load_image_file("px-woman-smilings.jpg")
codificacao_referencia_nivel3 = face_recognition.face_encodings(imagem_referencia_nivel3)[0]

# Inicialize a webcam
webcam = cv2.VideoCapture(0)

while True:
    ret, frame = webcam.read()

    if not ret:
        break

    # Converta o frame para RGB (necessário para face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detecte rostos no frame
    face_locations = face_recognition.face_locations(rgb_frame)
    if face_locations:
        # Codifique o rosto detectado
        codificacoes = face_recognition.face_encodings(rgb_frame, face_locations)

        for codificacao in codificacoes:
            # Compare a codificação do rosto com as imagens de referência dos diferentes níveis
            nivel_acesso = None

            # Nível 1
            if face_recognition.compare_faces([codificacao_referencia_nivel1], codificacao)[0]:
                nivel_acesso = "Nível 1 - Acesso permitido a todos"
            # Nível 2
            elif face_recognition.compare_faces([codificacao_referencia_nivel2], codificacao)[0]:
                nivel_acesso = "Nível 2 - Acesso restrito a diretores de divisões"
            # Nível 3
            elif face_recognition.compare_faces([codificacao_referencia_nivel3], codificacao)[0]:
                nivel_acesso = "Nível 3 - Acesso somente ao ministro do meio ambiente"

            # Exiba o nível de acesso na imagem
            if nivel_acesso:
                cv2.putText(frame, nivel_acesso, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exiba o frame
    cv2.imshow("Sistema de Segurança", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
