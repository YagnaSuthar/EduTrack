import csv   
import random
import string
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from student.models import student,Teacher,Marks,School,Standard,Subject,ClassSection,Message,Room,StudentSuggestion
from .teacher_chatbot import giveResponse_Teacher
from django.http import JsonResponse
from .get_suggesions import generate_suggestions_for_teacher,generate_suggestions_for_student,generate_subject_wise_suggestions_for_student
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,teacher_only,student_only,school_admin_only
from allauth.account.views import PasswordResetView,PasswordResetDoneView
from django.core.exceptions import ObjectDoesNotExist
from student.forms import standardForm ,classForm,SchoolForm,SubjectForm,MarkForm,MessageForm,RoomForm,FileUploadForm,StudentSuggestionForm
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.db.models import Avg
from student.models import Marks
from student.ml_utils import predict_student_performance
from django.db.models import Q
from django.contrib.auth.models import Group
# Create your views here.

from django.contrib.auth.decorators import user_passes_test

def generate_password(length=8):
    """Generate a random password."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


######################################################################### Error Handling #################################################################################################



                                                                            # pending #


# ######################################################################## Role based redirecting to the dashboard ##################################################################################



# Role based Rendering in templates - Avalible Roles =[Admin,Student,Teacher] - Same name Groups there 
def role_based_redirect(request):
    user = request.user

    if user.groups.filter(name="Student").exists():
        return redirect('student_dash')

    elif user.groups.filter(name="Teacher").exists():
        return redirect('teacher_dash')

    elif user.is_superuser:  # Admin check
         return  HttpResponse('admin-Dashboard')  # Change to your actual admin dashboard URL
    
    elif user.groups.filter(name="SchoolAdmin").exists():
        return redirect('schooladmin_dash')
    
    elif user.groups.filter(name="Admin").exists():
        return redirect('pending_requests')
    
    

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

@never_cache
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


@never_cache
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

@never_cache
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
@allowed_users(allowed_roles=['Teacher'])
@teacher_only
def student_data(request):
    q = request.GET.get('q') if request.GET.get('q') !=  None else ''
    students = student.objects.filter(
        Q(name__icontains=q)|
        Q(email__icontains=q) |
        Q(gender__icontains=q) | 
        Q(performance_summary__icontains=q)
        
    )

    group = get_user_role(request.user)
    print(group)
    # students = student.objects.all()
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


@login_required
@student_only
def student_suggessions(request,pk):
    student_obj = student.objects.get(student_id=pk)
    genrated_suggestion = generate_suggestions_for_student(student_obj.avg_sat_score,student_obj.avg_pat_score,student_obj.attendance,student_obj.performance_summary)
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

################################################################################### Upload Csv Functionality #############################################################################


































################################################################################### CSV - Genrator - FUNCTION ############################################################################# 
@login_required
@teacher_only
def export_students_csv_toteacher(request):
    students = student.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Email', 'Generated Password', 'Gender', 'Avg PAT Score', 'Avg SAT Score', 'Attendance', 'Performance'])

    for student_obj in students:
        writer.writerow([
            student_obj.name,
            student_obj.email,
            student_obj.raw_password if student_obj.raw_password else "N/A",  # ✅ Exact password
            student_obj.gender,
            student_obj.avg_pat_score,
            student_obj.avg_sat_score,
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
        # Extract the subject names into a list of strings
        subject_names = [subject.name for subject in teacher_obj.subject.all()]
        
        # Join the subject names into a single string, if you want to separate them by commas, for example
        subject_str = ", ".join(subject_names)
        writer.writerow([
            teacher_obj.name,
            teacher_obj.email,
            teacher_obj.raw_password if teacher_obj.raw_password else "N/A",
            teacher_obj.gender,
            subject_str
        ])
    return response



######################################################################## Uplod csv ##############################################################################################################
import io 
import PyPDF2
from django.contrib.auth.models import User

def upload_file_student_data(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST,request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']  # ✅ CORRECT
          
            if uploaded_file.name.endswith('.csv'):
                data_set = uploaded_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for row in csv.reader(io_string,delimiter=','):
                    print(row)
                    password = generate_password()
                    username = row[0]
                    email = row[1]
                    gender = row[2]
                    attendance = row[3]
                    avg_pat_score = row[4]
                    avg_sat_score = row[5]
                    user = User.objects.create_user(username=username, email=email, password=password)
                    
                    student_group = Group.objects.get(name='Student')  
                    user.groups.add(student_group)
                    user.save()
                
                    student.objects.create(
                        user= user,
                        name = username,
                        email = email,
                        gender = gender,
                        attendance = attendance,
                        raw_password = password,
                        avg_pat_score =avg_pat_score,
                        avg_sat_score = avg_sat_score,
                        performance_summary = predict_student_performance(
                                    gender,
                                    avg_sat_score,
                                    avg_pat_score,
                                    attendance
                            )[:20]  # Optional truncate
                    )

            elif uploaded_file.name.endswith('.pdf'):
                # pdf_data = uploaded_file.read()
                # pdf_stream = io.BytesIO(pdf_data)
                # reader = PyPDF2.PdfReader(pdf_stream)
                reader = PyPDF2.PdfReader(uploaded_file)
                print("Uploaded PDF: ", uploaded_file.name)
                # print("Number of pages: ", len(reader.pages))
                text = ""
                print(reader)
                
                for page in reader.pages:
                    text += page.extract_text()
                    print(text)

                for line in text.split("\n"):
                    print(line)
                    parts = line.split(",")

                    if len(parts) == 3:
                        try:
                            student.objects.create(
                                name = parts[0],
                                email = parts[1],
                                gender = parts[2]
                            )
                        except Exception as e:
                            print('Skipping line due to error',e)

        return redirect('student_data')

    else:
        form = FileUploadForm()
    return render(request,'student/student_list.html',{'form':form})



######################################################################### Custom context view modification to allauth ####################################################################


class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  # Get the default context

        # Safely check if the user is authenticated before querying student model
        user = self.request.user
        if user.is_authenticated:
            try:
                student_obj = student.objects.get(user=user)
                context['student'] = student_obj
                context['is_student'] = True
            except ObjectDoesNotExist:
                context['student'] = None
                context['is_student'] = False
            context['is_teacher'] = is_teacher(user)
            context['is_schooladmin'] = is_schooladmin(user)
        else:
            # For anonymous users (e.g., password reset)
            context['student'] = None
            context['is_student'] = False
            context['is_teacher'] = False
            context['is_schooladmin'] = False

        return context

    
class CustomePasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  # Get the default context
        user = self.request.user
        if user.is_authenticated:
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
        else:
            # For anonymous users (e.g., password reset)
            context['student'] = None
            context['is_student'] = False
            context['is_teacher'] = False
            context['is_schooladmin'] = False

        return context
    

######################################################################### School -admin approvel Registration #############################################

from student.models import SchoolAdminProfile
from django.contrib import messages
def pendingRequest(request):
    pending_requests = SchoolAdminProfile.objects.filter(approved = False)
    context = {
        'pending_requests':pending_requests,
    }
    return render(request,'Dashboard/Admin/pending_requests.html',context)

def approveScAdmin(request, user_id):
    school_admin = SchoolAdminProfile.objects.get(user_id=user_id)
    school_admin.approved = True
    school_admin.save()
    
    messages.success(request, "School Admin approved successfully!")
    return redirect('pending_requests')

################################################################# school-admin classes and standards #################################################

# creation-forms -> student -> views.py 

def standard_class_list(request):
    # school = School.objects.get(principal = request.user)
    standards = Standard.objects.all()
    subjects = Subject.objects.all()
    classes = ClassSection.objects.all()

    standards_count = standards.count()
    classes_count = classes.count()
    subjects_count = subjects.count()

    context ={
        'standards_count':standards_count,
        'classes_count':classes_count,
        'subjects_count':subjects_count,
        'standards':standards,
        'subjects':subjects,
        'classes':classes,
        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user),
        'is_schooladmin':is_schooladmin(request.user),
    }
    return render(request,'Dashboard/school_admin/standards_list.html',context)

def createStandard(request):
    form = standardForm()
    if request.method == 'POST':
        form = standardForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('standards_list')
        else:
            messages.error(request,'Error During Standard Creation')
        
    context = {
        'form':form,
        'is_schooladmin':is_schooladmin(request.user)
    }
    return render(request,'student/standard_create.html',context)

def createClassToParticularStandard(request):
    form = classForm()

    if request.method == 'POST':
        form  = classForm(request.POST)

        if form.is_valid:
            form.save()
            return redirect('standards_list')
        else:
            messages.error(request,'Error During class Association')

    context = {
        'form':form,
        'is_schooladmin':is_schooladmin(request.user),
    }
    return render(request,'student/class_create.html',context)




def add_school(request):
    form = SchoolForm()

    if request.method == "POST":
        form = SchoolForm(request.POST)

        if form.is_valid:
            form.save()
            return redirect('standards_list')
        else:
            messages.error(request,'Error during adding school')
    context = {
        'form':form,
        'is_schooladmin':is_schooladmin(request.user)

    }
    return render(request,'student/school_create.html',context)


def add_new_subject(request):
    form = SubjectForm()

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('standards_list')
        else:
            messages.error(request,'Error suring adding a new subject data')\
   
    context = {
        'form':form,
        'is_schooladmin':is_schooladmin(request.user)

    }    
    return render(request,'student/subject_create.html',context)





################################################## student marks subject wise views here  ############################################################

def add_student_marks(request, student_id):
    student_obj = get_object_or_404(student, student_id=student_id)
    teacher = get_object_or_404(Teacher, user=request.user)
    subjects = teacher.subject.all()

    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            if subject not in subjects:
                return render(request, 'unauthorized.html')

            mark, created = Marks.objects.get_or_create(student=student_obj, subject=subject)
            mark.pat_score = form.cleaned_data['pat_score']
            mark.sat_score = form.cleaned_data['sat_score']
            mark.marks_obtained = form.cleaned_data['marks_obtained']
            mark.added_by = request.user
            mark.save()

            # ✅ Recalculate averages
            all_marks = Marks.objects.filter(student=student_obj)
            avg_pat = all_marks.aggregate(Avg('pat_score'))['pat_score__avg'] or 0
            avg_sat = all_marks.aggregate(Avg('sat_score'))['sat_score__avg'] or 0

            student_obj.avg_pat_score = round(avg_pat, 2)
            student_obj.avg_sat_score = round(avg_sat, 2)

            # ✅ Predict performance again
            student_obj.performance_summary = predict_student_performance(
                student_obj.get_gender_display(),
                avg_sat,
                avg_pat,
                student_obj.attendance
            )[:20]  # Optional truncate

            student_obj.save()

            return redirect('student_list')
    else:
        form = MarkForm()

    return render(request, 'student/add_marks.html', {
        'form': form,
        'student': student_obj,
        'subjects': subjects
    })



def edit_student_marks(request, pk):
    user = request.user
    student_obj = get_object_or_404(student, student_id=pk)
    teacher = get_object_or_404(Teacher, user=request.user)
    subjects = teacher.subject.all()

    # Get the Marks object you want to edit
    try:
        mark_obj = Marks.objects.get(student=student_obj)  # You might need subject here too
    except Marks.DoesNotExist:
        mark_obj = None

    if request.method == "POST":
        form = MarkForm(request.POST, instance=mark_obj)
        if form.is_valid():
            mark = form.save(commit=False)

            if mark.subject not in subjects:
                return render(request, 'unauthorized.html')

            mark.student = student_obj
            mark.added_by = request.user
            mark.save()

            # ✅ Recalculate averages
            all_marks = Marks.objects.filter(student=student_obj)
            avg_pat = all_marks.aggregate(Avg('pat_score'))['pat_score__avg'] or 0
            avg_sat = all_marks.aggregate(Avg('sat_score'))['sat_score__avg'] or 0

            student_obj.avg_pat_score = round(avg_pat, 2)
            student_obj.avg_sat_score = round(avg_sat, 2)

            student_obj.performance_summary = predict_student_performance(
                student_obj.get_gender_display(),
                avg_sat,
                avg_pat,
                student_obj.attendance
            )[:20]

            student_obj.save()

            return redirect('student_list')
    else:
        form = MarkForm(instance=mark_obj)

    return render(request, 'student/add_marks.html', {
        'form': form,
        'student': student_obj,
        'subjects': subjects,
        'is_teacher':is_teacher(user),
        'is_student':is_student(user),
        'is_schooladmin':is_schooladmin(user),
    })

@login_required
@student_only
def subject_wise_marks(request, pk):
    student_obj = student.objects.get(student_id=pk)
    marks_set = Marks.objects.filter(student=student_obj)
    suggestions_from_teacher = StudentSuggestion.objects.filter(student=student_obj)

    subject_wise_suggestions = []  # Initialize an empty list to store suggestions

    for mark in marks_set:
        # Generate suggestion for each subject and append to the list
        subject_wise_suggestion = generate_subject_wise_suggestions_for_student(
            mark.subject.name, mark.sat_score, mark.pat_score)
        subject_wise_suggestions.append(subject_wise_suggestion[0])  # Only taking the first suggestion from the list

    context = {
        'subject_wise_suggestions': subject_wise_suggestions,  # Pass the list of suggestions
        'marks': marks_set,
        'student': student_obj,  # Pass the student object to the template
        'is_teacher': is_teacher(request.user),
        'is_student': is_student(request.user),
        'suggestions_from_teacher':suggestions_from_teacher
    }
    return render(request, 'student/student_marks.html', context)


@login_required
@student_only
def get_subject_suggestion(request):
    if request.method == 'GET':
        mark_id = request.GET.get('mark_id')
        subject = request.GET.get('subject')

        
        
        mark = Marks.objects.get(id=mark_id)
        # Assuming the suggestion generation function works as expected
        subject_wise_suggestion = generate_subject_wise_suggestions_for_student(
            subject, mark.sat_score, mark.pat_score
        )
        
        # Return the first suggestion (you can customize this to handle more than one suggestion)
        suggestion = subject_wise_suggestion if subject_wise_suggestion else "No suggestion available."
        print(suggestion)
        return JsonResponse({'suggestion': suggestion})



# ####################################################################### chat platform ########################################################################

def message_view(request,pk):

    messages = Message.objects.all()
    room = Room.objects.get(id=pk)
    room_participants = room.participants.all()
    role = get_user_role(request.user)
 
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body =  request.POST.get('body')    )
    
        room.participants.add(request.user)
        return redirect('chat',pk=room.id)
    
    
    context = {
   
        'room_participants':room_participants,
        'role':role,
        'messages':messages,
        'room':room,
        'is_schooladmin':is_schooladmin(request.user),
        'is_teacher':is_teacher(request.user),
    }
    return render(request,'chat/message.html',context)


def room_create(request):
    
    form = RoomForm()
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save(commit=False)
            
            form.user = request.user
            form.save()

        else: 
            return HttpResponse('Error here!')
    context = {
        'rooms':rooms,
        'form':form,
        'is_schooladmin':is_schooladmin(request.user),
        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user),
        
    }

    return render(request,'chat/chat.html',context)




def deleteStandard(request,pk):
    user = request.user
    standard_obj = Standard.objects.get(id=pk)
    if request.method == "POST":
        standard_obj.delete()
        return redirect('standards_list')

    context= {
        'obj':standard_obj,
        'is_schooladmin':is_schooladmin(user),
        'is_teacher':is_teacher(user),
        'is_student':is_student(user)
    }
    return render(request,'student/delete_standard.html',context)

########################################################################## Personalize teacher's suject wise suggestion to the student ####################################################3


def personalize_suggestion_from_teacher(request,pk):
    form = StudentSuggestionForm()
 
    # suggestion = None
    print(request.method)
    if request.method == "POST":
        form = StudentSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.teacher = Teacher.objects.get(user=request.user)
            suggestion.student = student.objects.get(student_id=pk)
            suggestion.save()
            return redirect('student_data')
        
        else:
            messages.error(request,'Error while giving a suggestion')

    context={
        'form':form,
        'is_teacher':is_teacher(request.user),
        'is_student':is_student(request.user),
        'is_schooladmin':is_schooladmin(request.user),
    }
    return render(request,'student/suggestion_from_teacher.html',context)
    # return HttpResponse('This is a suggestion form here')