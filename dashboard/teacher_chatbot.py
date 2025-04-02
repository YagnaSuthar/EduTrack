# from student.forms import teacher_response
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def giveResponse_Teacher(teacher_response):
    # Prepare the input prompt using the teacher's response
    prompt = f"""
    follow this formate:
    -use paragraph for responce
    - do not use bold text.
    - give answer in 5 6 line paragraph.
    Generate a thoughtful and professional response based on the following teacher input:
    '{teacher_response}'
    Respond as a chatbot, offering helpful or insightful advice based on the teacher's input.
    """

    # Call the Gemini API to generate a response
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(prompt)

    # Extract prediction from Gemini's response
    chatbot_response = response.text.strip()

    # Return the chatbot response
    return chatbot_response

