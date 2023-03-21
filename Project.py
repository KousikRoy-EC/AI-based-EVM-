import cv2
import serial
from simple_facerec import SimpleFacerec

ser = serial.Serial('COM4', 9600)
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    face_locations, face_names = sfr.detect_known_faces(frame)
    if (len(face_names) > 0):
        ser.write("auth\n".encode())
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
    else:
        ser.write("invalid\n".encode())

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        ser.write("invalid\n".encode())
        break


ser.close()
cap.release()
cv2.destroyAllWindows()
