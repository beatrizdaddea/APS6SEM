import cv2
import pickle
import face_recognition

cv2.namedWindow("Sistema de Seguranca", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Sistema de Seguranca", 800, 600)  

def predict(img_path, knn_clf=None, model_path=None, threshold=0.6):
    if knn_clf is None and model_path is None:
        raise Exception("Deve fornecer o classificador knn através de knn_clf ou model_path")
    # Carrega um modelo KNN treinado
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    # Carrega o arquivo de imagem e detecta os rostos
    imagem = img_path
    posicaoRosto = face_recognition.face_locations(imagem)
    # Se nenhum rosto for encontrado na imagem, retorna um resultado vazio.
    if len(posicaoRosto) == 0:
        return []
    # Encontra codificações para rostos na imagem de teste
    codificacoes = face_recognition.face_encodings(imagem, known_face_locations=posicaoRosto)
    # Usa o modelo KNN para encontrar a face que melhor corresponde
    menorDistancia = knn_clf.kneighbors(codificacoes, n_neighbors=2)
    corresponde = [menorDistancia[0][i][0] <= threshold for i in range(len(posicaoRosto))]
    # Preve classes e remove classificações que não estejam dentro do limite
    return [
        (predicao, local) 
        if rec 
        else 
            ("unknown", local) 
        for predicao, local, rec in zip(knn_clf.predict(codificacoes),posicaoRosto,corresponde)
    ]

# Inicia a webcam
webcam = cv2.VideoCapture(0)

while True:
    # Loop enquanto a câmera estiver funcionando
    verificar = False
    while(not verificar):
        # Coloca a imagem da webcam em 'frame'
        (verificar, frame) = webcam.read()
        if(not verificar):
            print("Falha ao abrir a WebCam. Tente novamente.")

    frame=cv2.flip(frame,1) # Inverte o sentido horizontal do frame
    frame_copy = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Converta a imagem da cor BGR (que o OpenCV usa) para a cor RGB (que o face_recognition usa)
    frame_copy=cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
    predictions = predict(frame_copy, model_path="classifier/trained_knn_model.clf")
    for name, (top, right, bottom, left) in predictions:
        # Redimensiona o quadro, pois ele foi dimensionado para 1/4 de tamanho
        top *= 4 
        right *= 4
        bottom *= 4
        left *= 4
        # Verifica quem é a pessoa reconhecida e atribui o nivel de acesso
        if name == "Beatriz":
            name += " - Nivel 1"
                        
        elif name == "Mateus":
            name += " - Nivel 2"

        elif name == "Rafael":
            name += " - Nivel 3"
            
        # Desenha o retângulo ao redor do rosto reconhecido junto ao nome
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom), (right, bottom + 35), (0, 0, 255), cv2.FILLED)
        fonte = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, bottom + 30), fonte, 0.6, (255, 255, 255), 1)
        
    cv2.imshow('Sistema de Seguranca', frame)
    
    if cv2.waitKey(5) == 27: # Encerra a aplicação com a tecla Esc
        break

webcam.release()
cv2.destroyAllWindows()
    
