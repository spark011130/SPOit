import cv2
import numpy as np
import mediapipe as mp
import pickle
import train_dataset_creator as pose

cap = cv2.VideoCapture(0)
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

detector = pose.poseDetector()

labels_dict = {0 : "Ball Out", 1 : 'No Signal', 2 : "Touch Out", 3 : "Overnet"}

while True:
    ret, frame = cap.read()
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = detector.findPose(img)
    positions = detector.findPosition(img)
    tmp = []
    for j in [12, 14, 16, 11, 13, 15]:
        tmp.extend(positions[j])

    prediction = model.predict([np.asarray(tmp)])
    print(prediction)
    predicted_character = labels_dict[int(prediction[0])]

    
    cv2.putText(img, f'detected pose : {predicted_character}', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('frame', img)
    k = cv2.waitKey(1)
    if k & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()
