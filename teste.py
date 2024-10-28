import face_recognition
import cv2
import numpy as np

# Carregar a imagem conhecida e extrair o encoding
known_image = face_recognition.load_image_file("conhecido.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]
known_face_encodings = [known_face_encoding]
known_face_names = ["Você"]

# Inicializar a câmera
video_capture = cv2.VideoCapture(0)

while True:
    # Captura um frame da câmera
    ret, frame = video_capture.read()

    # Reduz a imagem para processamento mais rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Localizar todos os rostos e codificá-los
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop pelos rostos detectados no frame da câmera
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Comparar o rosto detectado com a imagem conhecida
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        name = "Desconhecido"

        # Se houver uma correspondência, recuperar o índice do rosto
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Redimensionar as coordenadas de volta ao tamanho original
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenhar um retângulo em torno do rosto e exibir o nome
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Exibir o frame com a câmera ao vivo
    cv2.imshow("Video", frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar a câmera e fechar janelas
video_capture.release()
cv2.destroyAllWindows()
