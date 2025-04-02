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
        fields = ['name','first_name','last_name','email','subject','gender']

  

    # Use Checkboxes for selecting multiple subjects
    


# class TeacherResponse(ModelForm):
#     class Meta:
#         model = teacher_response
#         fields =['teacher_input']