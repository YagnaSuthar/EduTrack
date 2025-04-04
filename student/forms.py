from django.forms import ModelForm
from .models import student,Teacher
from django import forms
from django.contrib.auth.models import Group

class StudentForm(ModelForm):
    class Meta:
        model = student
        fields = ['name', 'gender', 'sat_score', 'pat_score', 'attendance','email']  # Exclude 'performance'
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            # user.set_password(self.cleaned_data["password"])
            user.save()
            student_group = Group.objects.get(name='Student')
            user.groups.add(student_group)
        return user


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name','email','subject','gender']

  

    # Use Checkboxes for selecting multiple subjects
    


# class TeacherResponse(ModelForm):
#     class Meta:
#         model = teacher_response
#         fields =['teacher_input']

from django import forms
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from .models import SchoolAdminProfile
from datetime import datetime

class CustomSignupForm(SignupForm):
    # full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    dob = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2025)))
    username = forms.CharField(max_length=150, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True, label="Gender")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    school_id = forms.FileField(required=True, label="Upload School ID Document")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        # Ensure the 'dob' is a valid date
        dob = cleaned_data.get('dob')
        if dob and isinstance(dob, str):
            try:
                # Try to convert to a valid date object if it's a string
                cleaned_data['dob'] = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Invalid date format. Please select a valid date.")

        return cleaned_data

    def save(self, request):
        user = super().save(request)
        
        # Ensure username is set (this is necessary since `django-allauth` 
        # might override the username with the email)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()

        # Create School Admin Profile
        school_admin_profile = SchoolAdminProfile(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            gender=self.cleaned_data['gender'],
            dob=self.cleaned_data['dob'],
            school_id=self.cleaned_data['school_id']
        )
        school_admin_profile.save()

        # Add user to the "SchoolAdmin" group
        school_admin_group = Group.objects.get(name='SchoolAdmin')
        user.groups.add(school_admin_group)

        return user