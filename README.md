# 🎓 EduTrack - Student Performance Predictor and Academic Tracker

EduTrack is a web-based academic performance monitoring and prediction system that uses machine learning (ANN) to analyze student data and provide personalized performance insights. It is designed to support educational institutions in tracking, predicting, and enhancing student outcomes using data-driven techniques.

---

## 🚀 Features

- 📊 **Student Performance Prediction** using ANN (Artificial Neural Network)
- 🏫 **School and Teacher Data Management** via CSV upload
- 📁 **Dynamic Dashboard** with academic statistics and visual insights
- 📤 **Bulk CSV Upload** for student records
- 📚 **Personalized Suggestions** for underperforming students
- 🔍 **Search and Filter** functionality for teachers and students
- 📦 Modular structure with reusable Django apps

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JS (via Django templates)
- **Machine Learning:** TensorFlow / Keras (ANN model)
- **Database:** SQLite (default) or PostgreSQL
- **Others:** Pandas, NumPy, Scikit-learn (for data preprocessing)

---

## 🧠 ML Model

The project uses an Artificial Neural Network (ANN) model to classify or predict student performance levels based on input academic and behavioral features. The model is trained and deployed inside the `studentPerformancePredictor` module.

---

## 📁 Project Structure
```
EduTrack/
│
├── dashboard/ # Admin/teacher dashboard logic
├── student/ # Student model, views, and data handling
├── studentPerformancePredictor/ # ML model training and prediction logic
├── templates/ # HTML Templates
├── static/ # CSS, JS, image files
├── media/school_ids/ # Uploaded CSVs and media
├── .vscode/ # Editor configs
├── manage.py # Django entry point
├── requirements.txt # Python dependencies
└── README.md # You're reading it!
```

---

## ⚙️ Installation & Setup

### 🔧 Prerequisites

- Python 3.8+
- Git
- pip / virtualenv

### 💻 Steps

# 1. Clone the repository
```bash
git clone https://github.com/YagnaSuthar/EduTrack.git
cd EduTrack
```
# 2. Create virtual environment & activate it
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

# 3. Install dependencies
```bash
pip install -r requirements.txt
```

# 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

# 5. Run the server
```bash
python manage.py runserver
```

📈 How to Use
Log in as admin or teacher.

Upload student/school/teacher CSVs.

View dashboard analytics.

Run prediction module to analyze student performance.

View personalized suggestions.

🧪 Sample CSV Format
StudentID,Name,Math,Science,English,Attendance,BehaviorScore
1,John,78,82,74,95,8
2,Alice,92,88,90,97,9
...
