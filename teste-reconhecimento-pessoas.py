import face_recognition
import cv2
import numpy as np

image_paths = ["conhecido.jpg"]
known_face_encodings = []
known_face_names = []

for image_path in image_paths:
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(image_path.split('/')[-1])

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

process_this_frame = True

while True:
    ret, frame = video_capture.read()

    if not ret:
        print("Falha ao capturar a imagem da câmera.")
        break

    frame = cv2.resize(frame, (640, 480))

    if process_this_frame:
        face_locations = face_recognition.face_locations(frame)
        unknown_face_encodings = face_recognition.face_encodings(frame)

        for (top, right, bottom, left), unknown_face_encoding in zip(face_locations, unknown_face_encodings):
            results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)

            name = "Desconhecido"
            if True in results:
                first_match_index = results.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    process_this_frame = not process_this_frame

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
