from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.homePage ,name="home"),
    path('student-data/',views.studentList,name='student_list'),
    path('create-student/',views.studentCreate,name='create_student'),
    path('create-Teacher/',views.TeacherCreate,name='create_teacher'),
    path('student/<int:pk>/',views.student),
    path('student_delete/<int:pk>/',views.studentDelete,name="student_delete"),
    # path('dashbord_teacher/',views.dashboard_layout,name='dashboard'),
    # path('predict/<int:student_id>/', views.predict_student_performance, name='predict_student'),
]
