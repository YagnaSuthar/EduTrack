import numpy as np 
import pandas as pd 
import tensorflow as tf 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix,accuracy_score

# importing the dataset 
dataset = pd.read_csv('student/ml/Data.csv')
X = dataset.iloc[:,3:-1].values 
y = dataset.iloc[:,-1].values

# Encoding the categorical data 
le = LabelEncoder()
ohe = OneHotEncoder(sparse_output=False)
X[:,0] = le.fit_transform(X[:,0])
y = ohe.fit_transform(y.reshape(-1,1))

#Train test split of the dataset
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
print(f"X_train:{X_train}")
print(f"X_test:{X_test}")

# Applying the Feature scaling to the splitted dataset 
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Building an ANN model 
# ann.add(tf.keras.layers.Dense(units=6,activation='relu'))
# ann.add(tf.keras.layers.Dense(units=6,avtivation='relu'))
# ann.add(tf.keras.layers.Dense(units=3,activation='softmax'))

ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=6,activation='relu'))
ann.add(tf.keras.layers.Dense(units=6,activation='relu'))
ann.add(tf.keras.layers.Dense(units=3,activation='softmax'))

#Training an ANN model 
ann.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
ann.fit(X_train,y_train,batch_size=32,epochs=100)

#predicting the y_pred 
y_pred = ann.predict(X_test)
y_test_labels = np.argmax(y_test,axis=1)
y_pred_labels = np.argmax(y_pred,axis=1)

print(f"y_pred is : {y_pred}")

#Cheaking the sccuracy of the model 
cm = confusion_matrix(y_test_labels,y_pred_labels)
print(cm)
print(accuracy_score(y_test_labels,y_pred_labels))
print(ann.evaluate(X_test,y_test))

ann.save("student_performance_ann_model.h5")

import joblib
joblib.dump(sc,'student/ml/scaler.pkl')
joblib.dump(le,'student/ml/label_encoder.pkl')
joblib.dump(ohe,'student/ml/encoder.pkl')