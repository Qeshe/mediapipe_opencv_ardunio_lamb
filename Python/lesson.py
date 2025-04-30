import cv2
import serial
import mediapipe as mp

# Arduino bağlantısı
arduino = serial.Serial('COM3', 9600)

# Mediapipe el tanıma modülü
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Parmak uçları id'leri (baş parmak, işaret parmağı, vs.)
tipIds = [4, 8, 12, 16, 20]

# PC kamerasını açıyoruz
cap = cv2.VideoCapture(0)

while True:
    succes, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lm_list = []  # Her eldeki parmakların koordinatlarını tutacak liste
    fingers = []  # Parmak açık mı kapalı mı listesi

    if results.multi_hand_landmarks:
        handlms = results.multi_hand_landmarks[0]

        # Koordinatları elde et
        for id, lm in enumerate(handlms.landmark):
            h, w, c = img.shape
            lm_list.append((int(lm.x * w), int(lm.y * h)))

        # El tipi (sağ mı sol mu)
        handType = results.multi_handedness[0].classification[0].label

        # Baş parmak kontrolü
        if handType == "Right":
            if lm_list[tipIds[0]][0] < lm_list[tipIds[0] - 1][0]:
                fingers.append(1)  # Açık
            else:
                fingers.append(0)  # Kapalı
        else:  # Sol el
            if lm_list[tipIds[0]][0] > lm_list[tipIds[0] - 1][0]:
                fingers.append(1)  # Açık
            else:
                fingers.append(0)  # Kapalı

        # Diğer parmaklar
        for id in range(1, 5):
            if lm_list[tipIds[id]][1] < lm_list[tipIds[id] - 2][1]:
                fingers.append(1)  # Açık
            else:
                fingers.append(0)  # Kapalı

        # Kaç parmak açık?
        totalFingers = fingers.count(1)
        print("Açık Parmaklar:", totalFingers)

        # Arduino'ya parmak sayısını gönder
        arduino.write(str(totalFingers).encode())  # Veriyi byte olarak gönderiyoruz

    # Kamerada resmi göster
    cv2.imshow("Image", img)
    
    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Kamera bağlantısını kapat
cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapat
