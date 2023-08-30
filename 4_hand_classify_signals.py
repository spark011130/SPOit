import cv2
import numpy as np
import mediapipe as mp
import pickle


cap = cv2.VideoCapture(0)
model_dict = pickle.load(open('./hand_model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode = True, min_detection_confidence= 0.2)

labels_dict = {0 : "double hit", 1 : "four hit", 2 : "double fault & Replay", 3: "nothing"}
predicted_character = "nothing"

while True:
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.flip(img_rgb, 1)
    results = hands.process(img_rgb)
    data_aux = []
    if results.multi_hand_landmarks:
        print("좋은데?")
        handclass = []
        for hand in results.multi_handedness:
            handclass.append(hand.classification[0].label)
        #1st hand_landmarks iteration : left
        #1st hand_landmarks iteration : right
        for hand_landmarks, hand_side in zip(results.multi_hand_landmarks, handclass):
            data_aux = []
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x); data_aux.append(y)
            no_predict = False
            if len(data_aux) == 42:
                data_aux = data_aux[21:]
            elif handclass[0] == 'Left':
                no_predict = True
            if not no_predict:
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]
                

                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]
    cv2.putText(img_rgb, f'detected pose : {predicted_character}', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                            cv2.LINE_AA)
    cv2.imshow('frame', img_rgb)
    k = cv2.waitKey(1)
    if k & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()
