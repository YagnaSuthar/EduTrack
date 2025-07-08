import joblib
import os
from django.conf import settings  # To access API Key
import google.generativeai as genai
from .models import student # Fix import (capitalize "Student")
from keras.models import load_model
from django.shortcuts import render
import numpy as np

# Load paths
MODEL_DIR = os.path.join(settings.BASE_DIR, 'student', 'ML')
model = load_model(os.path.join(MODEL_DIR, 'student_performance_ann_model.h5'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
label_encoder = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
onehot_encoder = joblib.load(os.path.join(MODEL_DIR, 'encoder.pkl'))



def predict_student_performance(gender, sat_score, pat_score, attendance):
    try:

        gender_encoded  = label_encoder.transform([gender])[0]
        X_input = np.array([[gender_encoded, sat_score, pat_score, attendance]])

        X_scaled = scaler.transform(X_input)

        y_pred= model.predict(X_scaled)

        predicted_category = onehot_encoder.inverse_transform(y_pred)[0][0]

        print(predicted_category)

        return predicted_category
    except Exception as e :
        print(f"[Error] prediction Failed{e}")
        return "Unknown"
