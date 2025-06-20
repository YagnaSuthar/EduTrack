from django.conf import settings  # To access API Key
import google.generativeai as genai


# Set up Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
def generate_suggestions_for_teacher(performance_level):
    # Construct a detailed input prompt for the model
    prompt = f"""
    You are a teacher providing recommendations for other teachers on how to improve the performance of students. Given the following information about a student, suggest specific tasks or strategies a teacher can use to help them improve their performance:

    Student details:
    - Student performance: {performance_level}

    Based on the student's scores and attendance, provide the teacher with ONE actionable task or strategy to:
    1. Improve their SAT and PAT scores.
    2. Increase attendance and motivation.
    3. Suggest any additional activities that could benefit the student.

    Follow this format:
    - Do not use bold text.
    - Provide the answer in a single paragraph.
    - Keep it concise, within 2-4 lines.
    - Do not enclose the response in brackets [""] or quotes.
    """

    # Call Gemini API
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(prompt)

    # Extract and clean the response
    suggestions_for_teacher = response.text.strip()

    # Ensure brackets [""] are removed if they appear
    if suggestions_for_teacher.startswith("[") and suggestions_for_teacher.endswith("]"):
        suggestions_for_teacher = suggestions_for_teacher[1:-1]  # Remove first and last character

    return suggestions_for_teacher  # Return as a clean string


def generate_suggestions_for_student(sat_score,pat_score,attendance,performance_level):
    # Construct a detailed input prompt for the model
    prompt = f"""
    You are a teacher or mentor providing recommendations for students based on their performance data. Given the following information about a student, suggest specific tasks or strategies they can use to improve their performance. Tailor your suggestions based on their SAT score, PAT score, attendance, and overall performance.

    Student details:
    
    - SAT score: {sat_score}
    - PAT score: {pat_score}
    - Attendance: {attendance}%
    - Performance level: {performance_level}

    **Start by printing the following data:**

    - SAT score: {sat_score}
    - PAT score: {pat_score}
    - Attendance: {attendance}%
    - Performance: {performance_level}

    **Based on the student's performance, provide ONE actionable recommendation in each of the following categories:**

    1. **Improving SAT and PAT scores**:
        - If the SAT score or PAT score is low, provide one suggestion focused on improving these scores (e.g., extra study sessions, practice tests, or targeted review of weak areas).
        - If the SAT or PAT score is high, suggest advanced study techniques or deeper learning.
    
    2. **Increasing attendance and motivation**:
        - If the attendance is low, suggest ways to improve motivation to attend classes, such as setting goals or providing incentives.

    3. **Additional activities**:
        - **If the performance is low**: Do not suggest extracurricular activities or competitions. Instead, focus on academic improvement strategies (e.g., tutoring, more focused study, time management).
        - **If the performance is high**: Suggest participating in academic competitions, challenges, or other extracurricular activities to enhance their learning and motivation (e.g., science fairs, debates, coding competitions in India).

    **REMEMBER:** Each suggestion must be concise, limited to only one sentence, and should not include any asterisks, commas, quotation marks, or Python code.
    """




    # Call Gemini API (assuming you have already configured it properly)
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(prompt)

    # Extract the suggestions from the response
    suggestions_for_teacher = response.text.strip()

    # If the response is long, split it into individual suggestions
    suggestions_list = suggestions_for_teacher.split("\n")

    # Return the suggestions
    return suggestions_list

def generate_subject_wise_suggestions_for_student(subject, sat_score, pat_score):
    # Constructing a detailed input prompt for the model with more general recommendations for any subject
    prompt = f"""
    You are a teacher or mentor providing personalized recommendations based on a student's performance. Given the student's subject, SAT score, and PAT score, print the subject name, SAT score, and PAT score first. Then, based on their scores, provide actionable and concise recommendations for improving the student's performance in that subject.

    **Student Performance Details:**
    - Subject: {subject}
    - SAT Score: {sat_score}
    - PAT Score: {pat_score}

    **Instructions:**
    1. Print the subject name followed by the SAT score and PAT score.
    2. Provide a recommendation based on the student's SAT and PAT scores:
        - If the **SAT score** is low (below 600), suggest extra practice with basic concepts, focusing on areas like problem-solving, practice tests, or review of key topics.
        - If the **SAT score** is high (above 700), recommend advanced practice, focusing on solving higher-level problems or understanding more complex concepts.
        - If the **PAT score** is low (below 60), suggest additional review of fundamental concepts and practice of core skills in the subject.
        - If the **PAT score** is high (above 70), recommend tackling more challenging tasks and enhancing understanding through complex questions or real-world applications of the subject.

    **Example Response:**
    Subject: Math
    SAT Score: 520
    PAT Score: 60
    Recommendation: "Focus on solving additional numerical problems and reviewing key concepts such as algebra and geometry. Practice problem-solving techniques to improve your SAT and PAT scores."

    **Response Format:**
    - Print the subject name, SAT score, and PAT score first.
    - Then provide the relevant suggestion based on the student's scores.
    - The suggestion should be brief and concise, focusing on practical, actionable steps.

    **Your Response:**
    """
    
    # Call Gemini API (assuming you have already configured it properly)
    model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
    response = model.generate_content(prompt)

    # Extract and clean up the suggestion from the model response
    suggestion = response.text.strip()

    # Return the suggestion
    return suggestion
