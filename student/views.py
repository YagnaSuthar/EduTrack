import random
import string
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import StudentForm,TeacherForm
from .models import student,Teacher
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from django.contrib.auth.decorators import login_required
from .ml_utils import predict_student_performance  # Use the correct function name
import csv
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from dashboard.decorators import unauthenticated_user
from dashboard.views import is_teacher,is_student,is_schooladmin

LOGIN_URL = settings.LOGIN_URL

# Create your views here.

# @staff_member_required(login_url=LOGIN_URL)
# @login_required
# @unauthenticated_user
def homePage(request):
    # if request.user.is_authenticated:
    #     # return student_home_dash(request)
    #     return redirect('/')
   
    return render(request,'layout/main.html')


@user_passes_test(is_teacher)
def studentList(request):
    students = student.objects.all()
    context ={
        'students':students,
        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user),
    }
    return render(request,'student/student_list.html',context)
    



# def studentCreate(request):
#     form = StudentForm()
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)  # Don't save immediately

#             # Call Gemini API to predict performance
#             student.performance_summary = predict_student_performance(
#               student.get_gender_display(), student.sat_score, student.pat_score, student.attendance
#             )[:20]  

#             student.save()  # Save with predicted performance
#             return redirect('student_list')  # Redirect to student list page
        
#     context = {'form': form}
#     return render(request, 'student/student_create.html', context)


# ✅ Define generate_password as a standalone function
def generate_password(length=8):
    """Generate a random password."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def studentCreate(request):
    form = StudentForm()
    
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student_obj = form.save(commit=False)  # Don't save immediately

            # Use the email entered by the teacher
            email = student_obj.email

            # ✅ Generate password and store the raw version
            password = generate_password()
            print(password)
            student_obj.raw_password = password  # ✅ Save raw password
            print(student_obj.raw_password)
            print(student_obj.name)
            student_obj.save()  # ✅ Save first to generate student_id

            username = f"{student_obj.first_name.lower()}{student_obj.name}"
            # Create Django User account with hashed password
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()


            student_group = Group.objects.get(name='Student')  
            user.groups.add(student_group)

            # Link the User account to the student
            student_obj.user = user  

            # Call Gemini API to predict performance
            student_obj.performance_summary = predict_student_performance(
                student_obj.get_gender_display(), 
                student_obj.sat_score, 
                student_obj.pat_score, 
                student_obj.attendance
            )[:20]  

            student_obj.save()  # Save student with credentials

            return redirect('student_list')  # Redirect to student list page
        
    context = {'form': form,
                'is_teacher':is_teacher(request.user),
                'is_student':is_student(request.user),
                }
    return render(request, 'student/student_create.html', context)


def TeacherCreate(request):
    form = TeacherForm()
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid:


            teacher_obj = form.save(commit=False)
            # username = teacher_obj.name
            email = teacher_obj.email

            password = generate_password()
            teacher_obj.raw_password = password
            print(password)
            print(teacher_obj.raw_password)
            teacher_obj.save()

            username = f"{teacher_obj.name.lower()}"
            user = User.objects.create_user(username = username,email=email,password=password)
            user.save()

            teacher_group = Group.objects.get(name='Teacher')
            user.groups.add(teacher_group)


            teacher_obj.user = user 

            
            teacher_obj.save()
            form.save_m2m()
        
            return redirect('teacher_data')
    context={
        'form':form,
        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user),
        'is_schooladmin':is_schooladmin(request.user),
    }

    
    return render(request,'student/teacher_create.html',context)

def studentDelete(request,pk):
    
    Student = student.objects.get(student_id=pk)
    if request.method == "POST":
        Student.delete()
        return redirect('student_list')
    
    context={
        'Student':Student
    }
        
    return render(request,'student/delete_student.html',{'obj':Student})







########## new changes 
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import CustomSignupForm
from .models import SchoolAdminProfile
class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def dispatch(self, *args, **kwargs):
        """
        Restrict the signup page to only be accessible by school admins.
        For example, if you want to only allow admins to register through this form, you can
        add additional checks here (e.g., check for a specific permission or role).
        """
        if not self.request.user.is_authenticated or not self.request.user.is_superuser:
            # You can add more specific checks for admins here, or use permissions
            return HttpResponseForbidden("You are not authorized to access this page.")
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        # Redirect to a success page (e.g., dashboard or home page)
        return '/'  # Change this to your desired success URL
    

from django.contrib import messages 


@unauthenticated_user
def register_school_admin(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST, request.FILES)

        if form.is_valid():
            # Form is valid, save the user and profile
            form.save(request)
            messages.success(request, "Registration successful. Your account is under review.")
            return redirect('home')  # Make sure 'success_url' is valid
        else:
            # Print form errors to debug
            print("Form errors:", form.errors)
            messages.error(request, "There was an error with your registration form. Please check the details and try again.")
    
    else:
        form = CustomSignupForm()

    return render(request, 'Dashboard/school_admin/register.html', {'form': form})