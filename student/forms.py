from django.forms import ModelForm
from .models import student,Teacher,School,Standard,Subject,ClassSection,Marks,Message,Room
from django import forms
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from .models import SchoolAdminProfile
from datetime import datetime
class StudentForm(ModelForm):
    class Meta:
        model = student
        fields = ['name', 'gender', 'attendance', 'email', 'standard_class']  # 'subject' removed

    standard_class = forms.ModelMultipleChoiceField(
        queryset=ClassSection.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def save(self, commit=True):
        student_instance = super().save(commit=False)

        if commit:
            student_instance.save()
            self.save_m2m()

            # Add student to 'Student' group if user is linked
            student_group = Group.objects.get(name='Student')
            if student_instance.user:
                student_instance.user.groups.add(student_group)

            # Extract standards from selected classes
            selected_standards = Standard.objects.filter(
                classsection__in=student_instance.standard_class.all()
            ).distinct()

            # Assign these standards to the student
            student_instance.standard.set(selected_standards)

            # Get subjects for those standards
            related_subjects = Subject.objects.filter(standard__in=selected_standards).distinct()
            student_instance.subject.set(related_subjects)

        return student_instance



class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name','email','gender','subject','standard_class']

  
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    # standard = forms.ModelMultipleChoiceField(
    #     queryset=Standard.objects.all(), 
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )
    standard_class= forms.ModelMultipleChoiceField(
        queryset=ClassSection.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    # Use Checkboxes for selecting multiple subjects
    


# class TeacherResponse(ModelForm):
#     class Meta:
#         model = teacher_response
#         fields =['teacher_input']

class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    dob = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2025)))
    username = forms.CharField(max_length=150, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True, label="Gender")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    school_id = forms.FileField(required=True, label="Upload School ID Document")
    
    # School-related fields
    school_name = forms.CharField(max_length=100, required=True, label="School Name")
    school_address = forms.CharField(widget=forms.Textarea, required=True, label="School Address")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        dob = cleaned_data.get('dob')
        if dob and isinstance(dob, str):
            try:
                cleaned_data['dob'] = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Invalid date format. Please select a valid date.")

        return cleaned_data

    def save(self, request):
        user = super().save(request)
        
        # Set the username explicitly as it might be overridden by django-allauth
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()

        # Create the School Admin Profile
        school_admin_profile = SchoolAdminProfile(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            gender=self.cleaned_data['gender'],
            dob=self.cleaned_data['dob'],
            school_id=self.cleaned_data['school_id']
        )
        school_admin_profile.save()

        # Create the School with the current user as the principal
        school = School(
            name=self.cleaned_data['school_name'],
            address=self.cleaned_data['school_address'],
            principal=school_admin_profile  # Set the principal as the current user's profile
        )
        school.save()

        # Add user to the "SchoolAdmin" group
        school_admin_group = Group.objects.get(name='SchoolAdmin')
        user.groups.add(school_admin_group)

        return user
class standardForm(ModelForm):
    class Meta:
        model = Standard
        fields = '__all__'

class classForm(ModelForm):
    class Meta:
        model =ClassSection
        fields ='__all__'

class SchoolForm(ModelForm):
    class Meta:
        model = School
        fields = '__all__'

class SubjectForm(ModelForm):
    class Meta:
        model =Subject
        fields = '__all__'


class MarkForm(ModelForm):
    class Meta:
        model = Marks
        fields = [
            'subject',
            'pat_score',
            'sat_score',
            'marks_obtained'
        ]


# Messages and chats handling form 

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants']