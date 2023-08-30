import os
import mediapipe as mp
import cv2
import pickle

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode = True, min_detection_confidence= 0.2, max_num_hands = 2)

DATA_DIR = './data_hand'

data = []
labels = []

for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
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
                if len(data_aux) == 21:
                    if handclass[0] == 'Left':
                        data_aux = data_aux + [-1]*21
                    elif handclass[0] == 'Right':
                        data_aux = [-1]*21 + data_aux
                data.append(data_aux)
                labels.append(dir_)
print(len(data))
f = open('hand_data.pickle', 'wb')
pickle.dump({'data' : data,  'labels' : labels}, f)
f.close()