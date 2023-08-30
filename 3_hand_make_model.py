#train classifier
import pickle 
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data_dict = pickle.load(open('./hand_data.pickle', 'rb'))

print(len(data_dict['data']), len(data_dict['data'][0]))
print(len(data_dict['labels']))
data = np.asarray(data_dict['data'], dtype = object)
labels = np.asarray(data_dict['labels'])

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify = labels)
first = True
for xt, yt in zip(x_train, y_train):
    if len(xt) != 42 and first:
        for x in xt:
            print(x)
            first = False
        print(len(xt))
model = RandomForestClassifier()
model.fit(x_train, y_train)

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('{}% of samles were classified correctly !'.format(score*100))

f = open('hand_model.p', 'wb')
pickle.dump({'model' : model}, f)
f.close()