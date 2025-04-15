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
    path('standards-classes/',views.standard_class_list,name='standards_list'),
    path('standard-create-form/',views.createStandard,name='standard_create'),
    path('standard-delete-form/<int:pk>/',views.deleteStandard,name='standard_delete'),
    path('class-standard-association/',views.createClassToParticularStandard,name='class_create'),
    path('add-school/',views.add_school,name='school_create'),
    path('add-subject',views.add_new_subject,name='subject_create'),

    # Teacher - DashBoard Urls
    path('teacher_home/',views.teacher_home_dash,name='teacher_dash'),
    path('teacher-suggesions/',views.Teacher_suggesions,name="suggesions"),
    path('export-csv-forteacher/', views.export_students_csv_toteacher, name='export_students_csv'),
    path('teacherchatbot/',views.teacherchatbot,name="chatbot"),
    path('student_data/',views.student_data,name="student_data"),
    path('add-marks/<int:student_id>/', views.add_student_marks, name='add_marks'),
    path('Edit-marks/<int:pk>/', views.edit_student_marks, name='edit_marks'),
    path('upload-file/',views.upload_file_student_data,name='upload_file'),
    path('personalize-suggestion/<int:pk>/',views.personalize_suggestion_from_teacher,name='personalize_suggestion'),



    #  Student - Dashboard Urls
    path('student_home',views.student_home_dash,name="student_dash"),
    path('student-marks/<int:pk>/',views.subject_wise_marks,name='student_marks'),
    path('student-suggestion/<int:pk>/',views.student_suggessions,name='student_suggesions'),
    path('get_subject_suggestion/', views.get_subject_suggestion, name='get_subject_suggestion'),

    # Notifications - chat platform 
    path('chat/<int:pk>/',views.message_view,name='chat'),
    path('Room-create/',views.room_create,name='room_create'),


    
    ]