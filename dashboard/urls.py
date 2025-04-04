from .import views 
from django.urls import path,include



urlpatterns = [

    #  Role based redirection to the disred url or render view ['Admin','Teacher','Student']
    path('redirect/', views.role_based_redirect, name='role_based_redirect'),


    # Main admin which will approve school-admin profile - part of Admin group 
    path('admin_pending_request/',views.pendingRequest,name='pending_requests'),
    path('approve_school_admin/<int:user_id>/', views.approveScAdmin, name='approve_scadmin'),


    # School - Admin Dashboard urls 
    path('schooladmin_home',views.schooladmin_home_dash,name='schooladmin_dash'),
    path('teacher-list',views.TeacherList,name='teacher_data'),
    path('export-csv-forschooladmin/', views.export_teachers_csv_toschooladmin, name='export_teacher_csv'),


    # Teacher - DashBoard Urls

    path('teacher_home/',views.teacher_home_dash,name='teacher_dash'),
    path('teacher-suggesions/',views.Teacher_suggesions,name="suggesions"),
    path('export-csv-forteacher/', views.export_students_csv_toteacher, name='export_students_csv'),
    path('teacherchatbot/',views.teacherchatbot,name="chatbot"),
    path('student_data/',views.student_data,name="student_data"),


    #  Student - Dashboard Urls
    # path('',views.student_home_dash,name='dashboard-home'),
    path('student_home',views.student_home_dash,name="student_dash"),
    path('student-marks/<int:pk>/',views.student_marks,name='student_marks'),
    path('student-suggestion/<int:pk>/',views.student_suggessions,name='student_suggesions'),




    
    
    
    ]