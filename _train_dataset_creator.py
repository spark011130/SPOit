import cv2
import mediapipe as mp
import os
import pickle
import time

class poseDetector() :
    
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        
        self.mode = mode 
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon)
        
        
    def findPose (self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)    
        return img
    
    def findPosition(self, img, draw=False):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                #finding height, width of the image printed
                h, w, color = img.shape
                #Determining the pixels of the landmarks
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
        return lmList

def main():
    detector = poseDetector()
    cap = cv2.VideoCapture(0)

    dataset_size = 100
    number_of_classes = 4
    DATA_DIR = './data'

    data = []
    labels = []
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for i in range(number_of_classes):
        if not os.path.exists(os.path.join(DATA_DIR, str(i))):
            os.makedirs(os.path.join(DATA_DIR, str(i)))

        while True:  
            ret, img = cap.read() #ret is just the return variable, not much in there that we will use. 
            img = detector.findPose(img)
            cv2.putText(img, f'press "q", {i+1}th iteration ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
            cv2.imshow('frame', img)
            if cv2.waitKey(25) == ord('q'):
                break
        time.sleep(1)
        counter = 0
        while counter < dataset_size:
            ret, img = cap.read()
            cv2.imwrite(os.path.join(DATA_DIR, str(i), '{}.jpg'.format(counter)), img)
            img = detector.findPose(img)
            cv2.imshow('frame', img)
            positions = detector.findPosition(img)
            tmp = []
            for j in [12, 14, 16, 11, 13, 15]:
                tmp.extend(positions[j])
            data.append(tmp)
            # data.extend([positions[12], positions[14], positions[16], positions[11], positions[13], positions[15]])
            labels.append(i)
            cv2.waitKey(8)
            counter += 1

    for row in data:
        print(row)
    print(labels)
    cap.release()
    cv2.destroyAllWindows()
    
    f = open('data.pickle', 'wb')
    pickle.dump({'data' : data, 'labels' : labels}, f)
    f.close()

if __name__ == "__main__":
    main()