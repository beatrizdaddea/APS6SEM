import os
import math
from sklearn import neighbors
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pickle

def train(train_dir, model_save_path, n_neighbors=2, knn_algo='ball_tree', verbose=False):
    X = []
    y = []
    # Loop para cada pessoa no conjunto de treinamento
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue
        # Percorre cada imagem de treinamento da pessoa atual
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)
            print( "Processando :",img_path)
            if len(face_bounding_boxes) != 1:
                # Se não houver pessoas ou houver muitas pessoas em uma imagem de treinamento pula a imagem.
                if verbose:
                    print("A imagem {} não é adequada para o treinamento: {}".format(img_path, "Não foi detectado nenhum rosto" if len(face_bounding_boxes) < 1 else "Existe mais de um rosto na imagem"))
            else:
                # Adiciona a codificação facial para a imagem atual ao conjunto de treinamento
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determina quantos vizinhos usar para ponderação no classificador KNN
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Escolha n_neighbors automaticamente:", n_neighbors)
    # Cria e treina o classificador KNN
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)
    # Salva o classificador KNN treinado
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
        print("Treinamento completo")
    return knn_clf
train("train_img", "classifier/trained_knn_model.clf")

