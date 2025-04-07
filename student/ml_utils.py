from django.conf import settings  # To access API Key
import google.generativeai as genai
from .models import student # Fix import (capitalize "Student")

# Set up Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def predict_student_performance(gender, avg_sat_score, avg_pat_score, attendance):
    # Prepare the input prompt
    prompt = f"""
    Predict the student's performance as one of the following:
    - Low
    - Medium
    - High

    Student details:
    - Gender: {gender}
    - SAT Score: {avg_sat_score}
    - PAT Score: {avg_pat_score}
    - Attendance: {attendance}%

    Return **only one word** (Low, Medium, or High). Do not include any explanations.
    """

    # Call Gemini API
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    # Extract prediction from Gemini's response
    predicted_performance = response.text.strip().split()[0]  # Take only the first word

    return predicted_performance  # Return prediction as a string
