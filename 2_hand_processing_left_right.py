import os
import mediapipe as mp
import cv2
import pickle

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode = True, min_detection_confidence= 0.3)

DATA_DIR = './data_hand'

left_data = []
right_data = []
labels = []

for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data_aux = []
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            handclass = []
            for hand in results.multi_handedness:
                handclass.append(hand.classification[0].label)
            #1st hand_landmarks iteration : left
            #1st hand_landmarks iteration : right
            for hand_landmarks, hand_side in zip(results.multi_hand_landmarks, handclass):
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x); data_aux.append(y)
                if hand_side == 'Left':
                    left_data.append(data_aux)
                elif hand_side == 'Right':
                    right_data.append(data_aux)
                labels.append(dir_)
f = open('hand_data.pickle', 'wb')
pickle.dump({'left_data' : left_data, 'right_data' : right_data, 'labels' : labels}, f)
f.close()