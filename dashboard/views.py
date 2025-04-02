import csv   
from django.shortcuts import render,redirect,HttpResponse
from student.models import student,Teacher
from .teacher_chatbot import giveResponse_Teacher
from django.http import JsonResponse
from .get_suggesions import generate_suggestions_for_teacher,generate_suggestions_for_student
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,teacher_only,student_only,school_admin_only
from allauth.account.views import PasswordResetView,PasswordResetDoneView
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

from django.contrib.auth.decorators import user_passes_test


# ######################################################################## Role based redirecting to the dashboard ##################################################################################



# Role based Rendering in templates - Avalible Roles =[Admin,Student,Teacher] - Same name Groups there 
def role_based_redirect(request):
    user = request.user

    if user.groups.filter(name="Student").exists():
        return redirect('student_dash')
        
        # return render(request,'Dashboard/student/student_dash.html')  # Change to your actual student dashboard URL

    elif user.groups.filter(name="Teacher").exists():
        return redirect('teacher_dash')
       
        # return render(request,'student/teacher_list.html')  # Change to your actual teacher dashboard URL

    elif user.is_superuser:  # Admin check
         return  HttpResponse('admin-Dashboard')  # Change to your actual admin dashboard URL
    
    elif user.groups.filter(name="SchoolAdmin").exists():
        return redirect('schooladmin_dash')
    
    
    

    return redirect('/')  # Default fallback




##############################################################################  HOME PAGE ROLE VISE ################################################################################################

def get_user_role(user):
    """Return the role of the user (their group name)."""
    group_names = user.groups.values_list('name', flat=True)  # Get all group names
    return ", ".join(group_names) 

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()
def is_SchoolAdmin(user):
    return user.groups.filter(name='SchoolAdmin').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()
def is_schooladmin(user):
    return user.groups.filter(name='SchoolAdmin').exists()

@login_required
@school_admin_only
def schooladmin_home_dash(request):
    user = request.user
    user_role = get_user_role(user)
    print(user_role)
    context = {
        "user_role":user_role,
        "is_schooladmin":is_schooladmin(user)
    }
    return render(request,'Dashboard/school_admin/schooladmin_main_dash_home.html',context)



@login_required
@teacher_only
def teacher_home_dash(request):
    user = request.user
    user_role = get_user_role(request.user)
    if  user.groups.filter(name='Teacher').exists():

        context= {
            'is_teacher':is_teacher(user),
            'is_student':is_student(user)
        }


        return render(request,'Dashboard/teacher/teacher_main_dash_home.html',context)
    
    else:
        return HttpResponse(f"You are not allowed here {request.user}, Role - {user_role}")


@login_required
@student_only
@allowed_users(allowed_roles=['Student'])
def student_home_dash(request):
    user = request.user
    user_role = get_user_role(request.user)

    # Fetch the student object for the logged-in user
    student_obj = student.objects.get(user=user)

    if user.groups.filter(name='Student').exists():
        context = {
            'student': student_obj,  # Pass the student object to the template
            'is_teacher':is_teacher(user),
            'is_student':is_student(user)
        }
        return render(request, 'Dashboard/student/student_dash_main_home.html', context)
    else:
        return HttpResponse(f"You are not allowed here {request.user}, Role - {user_role}")










################################################################################ SHOW DATA TO PARTICULAR PAGE ############################################################################ 
@login_required
@allowed_users(allowed_roles='Student')
def student_marks(request,pk):
    student_obj = student.objects.get(student_id = pk)
    user =request.user
    print(student_obj)
    context = {
            'student': student_obj,  # Pass the student object to the template
            'is_teacher':is_teacher(user),
            'is_student':is_student(user)
        }
    return render(request, 'student/student_marks.html', context)


@login_required
@allowed_users(allowed_roles=['Teacher'])
@teacher_only
def student_data(request):

    group = get_user_role(request.user)
    print(group)
    students = student.objects.all()
    context ={
        'students':students,
        'is_teacher':is_teacher(request.user)
        

    }
    return render(request,'student/student_list.html',context)

@login_required
@school_admin_only
def TeacherList(request):
    teachers = Teacher.objects.all()
    user = request.user
    context ={
        'teachers':teachers,
        'is_teacher':is_teacher(user),
        'is_student':is_student(user),
        'is_schooladmin':is_schooladmin(user),

    }
    return render(request,'student/teacher_list.html',context)






# ############################################################################### AI - DRIVEN - CHATBOT ######################################################################################### 
@login_required
# @user_passes_test(is_teacher)
@teacher_only
# def teacherchatbot(request):
#     # form = teacher_response()
#     chatbot_response = None
#     teacher_response = None 
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#         # Get the user input from the form
#             teacher_response = request.POST.get('teacher_response')
        
#         if teacher_response:
#             # Use the teacher's response to get the chatbot response
#             chatbot_response = giveResponse_Teacher(teacher_response)
#             # return JsonResponse({'chatbot_response': chatbot_response})
        
#     print(teacher_response)
#     print(chatbot_response)


#     user = request.user

#     context={
#         'teacher_response':teacher_response,
#         # 'form':form,
#         'chatbot_response':chatbot_response,
         
#         'is_teacher':is_teacher(user),
#         'is_student':is_student(user)
     
#     }
#     return render(request,"Dashboard/teacher/chatbot.html",context)
    
def teacherchatbot(request):
    if not request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        teacher_response = request.POST.get('teacher_response')
        if teacher_response:
            try:
                chatbot_response = giveResponse_Teacher(teacher_response)
                
                # Return JSON response for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'chatbot_response': chatbot_response,
                        'status': 'success'
                    })
                    
                # For non-AJAX POST requests, render the template with context
                context = {
                    'teacher_response': teacher_response,
                    'chatbot_response': chatbot_response,
                    'is_teacher':is_teacher(request.user),
                    'is_student':is_student(request.user)
                }
                return render(request, "Dashboard/teacher/chatbot.html", context)
                
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'error': str(e),
                        'status': 'error'
                    }, status=500)
                return render(request, "Dashboard/teacher/chatbot.html", {'error': str(e)})
            
    context={

        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user)
     
    }
                    
    # For GET requests
    return render(request, "Dashboard/teacher/chatbot.html",context)
 





##################################################################################### ROLE - VISE - SUGGESIONS #######################################################################
@login_required
@teacher_only
def Teacher_suggesions(request):
    performance_level = request.GET.get('performance',None)  # Get filter from query parameters
    show_suggestion = False
    students = student.objects.all()
    suggestions = "none"
    
    if performance_level == "Low":
        students = student.objects.filter(performance_summary=performance_level)
        show_suggestion = True  # Indicate that suggestions should be shown for low performers
    elif performance_level == "Medium":
        students = student.objects.filter(performance_summary=performance_level)
        show_suggestion = True
    elif performance_level == "High":
        students = student.objects.filter(performance_summary=performance_level)
        show_suggestion = True
    else:
        students = student.objects.all()  # Show all if no filter is applied

    if show_suggestion:
        suggestions = generate_suggestions_for_teacher(performance_level)
        # suggestions = generate_suggestions_for_teacher(performance_level,students)
    context= {
            'is_teacher':is_teacher(request.user),
            'is_student':is_student(request.user),
            'students': students,
            'show_suggestion': show_suggestion,
            'performance_level':performance_level,
            'suggestions':suggestions
        }
    # print(students)
    print(performance_level)
    return render(request,'Dashboard/teacher/teacher_suggesions.html',context)

# older function for csv writer 
# def export_students_csv(request):
#     students = student.objects.all()

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="students_data.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Student Name', 'Email', 'Generated Password', 'Gender', 'PAT Score', 'SAT Score', 'Attendance', 'Performance'])

#     for student_obj in students:
#         writer.writerow([
#             student_obj.name,
#             student_obj.email,
#             student_obj.user.password,  # The hashed password
#             student_obj.gender,
#             student_obj.pat_score,
#             student_obj.sat_score,
#             student_obj.attendance,
#             student_obj.performance_summary
#         ])

#     return response

@login_required
@student_only
def student_suggessions(request,pk):
    student_obj = student.objects.get(student_id=pk)
    genrated_suggestion = generate_suggestions_for_student(student_obj.sat_score,student_obj.pat_score,student_obj.attendance,student_obj.performance_summary)
    print(genrated_suggestion)
    # return HttpResponse('genrates suggestion for given student - DONE')
    context ={
        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user),
        'student': student_obj,
        'suggestions':genrated_suggestion,
        'performance_level':student_obj.performance_summary
    }
    return render(request,'Dashboard/student/student_suggesions.html',context)





################################################################################### CSV - Genrator - FUNCTION ############################################################################# 
@login_required
@teacher_only
def export_students_csv_toteacher(request):
    students = student.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Email', 'Generated Password', 'Gender', 'PAT Score', 'SAT Score', 'Attendance', 'Performance'])

    for student_obj in students:
        writer.writerow([
            student_obj.name,
            student_obj.email,
            student_obj.raw_password if student_obj.raw_password else "N/A",  # ✅ Exact password
            student_obj.gender,
            student_obj.pat_score,
            student_obj.sat_score,
            student_obj.attendance,
            student_obj.performance_summary
        ])

    return response


@login_required
@school_admin_only
def export_teachers_csv_toschooladmin(request):
    Teachers = Teacher.objects.all()

    response = HttpResponse(content_type = 'text/scv')
    response['Content-Disposition'] = 'attachment; filename="teachers_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Teacher Name','Email','Genrated password','Gender','subject'])

    for teacher_obj in Teachers:
        writer.writerow([
            teacher_obj.name,
            teacher_obj.email,
            teacher_obj.raw_password if teacher_obj.raw_password else "N/A",
            teacher_obj.gender,
            teacher_obj.subject
        ])
    return response



######################################################################### Custom context view modification to allauth ####################################################################



class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  # Get the default context

        # Check if the user is a student
        try:
            student_obj = student.objects.get(user=self.request.user)
            context['student'] = student_obj
            context['is_student'] = True
        except ObjectDoesNotExist:
            context['is_student'] = False  # If no student exists, set to False
            context['student'] = None

        # Add your custom context variables here
        context['is_teacher'] = is_teacher(self.request.user)

        return context
    
class CustomePasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  # Get the default context

       # Check if the user is a student
        try:
            student_obj = student.objects.get(user=self.request.user)
            context['student'] = student_obj
            context['is_student'] = True
        except ObjectDoesNotExist:
            context['is_student'] = False  # If no student exists, set to False
            context['student'] = None

        # Add your custom context variables here
        context['is_teacher'] = is_teacher(self.request.user)

        return context
    
