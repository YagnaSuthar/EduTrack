from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()
# Create your models here.

class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    # SUBJECT_CHOICES = [('physics','physics'),('maths','maths'),('chemistry','chemistry')]
    SUBJECT_CHOICES = [
        ('p', 'Physics'),
        ('m', 'Maths'),
        ('c', 'Chemistry'),
    ]

    teacher_id= models.AutoField(primary_key=True)
    subject = models.CharField(max_length=10,choices=SUBJECT_CHOICES,default='Unknown')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='O')  # Use 'O' (Other) as default
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    raw_password = models.CharField(max_length=20,null=True,blank=True)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# class Subject(models.Model):
#     SUBJECT_CHOICES = [('p','physics'),('m','maths'),('c','chemistry')]
#     subject = models.CharField(max_length=1,choices=SUBJECT_CHOICES,default='Unknown')
#     # name = models.CharField(max_length=100)

class student(models.Model):

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,max_length=30, default='abc@gmail.com')
    date_of_birth = models.DateField(default='2000-01-01')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')  # Use 'O' (Other) as default
    attendance = models.IntegerField()  # Remove max_length
    pat_score = models.IntegerField()  # Remove max_length
    sat_score = models.IntegerField()  # Remove max_length
    raw_password = models.CharField(max_length=20, null=True, blank=True)  
    
    # Store the predicted performance
    performance_summary = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):  
        return f"{self.first_name} {self.last_name}"



    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    # def generate_password(self, length=8):
    #     """Generate a random password"""
    #     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# class teacher_response(models.Model):
#     teacher_input = models.CharField(max_length=50)


# srudent ->
#       student_id (Unique for all the students)
#       name (FirstName,LastName)
#       Email(Email Verification SMTP)
#       DOB
#       in views - student create and delete(CRUD) & read (performance) options are there


    