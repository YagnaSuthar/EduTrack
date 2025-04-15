from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()
# Create your models here.

class SchoolAdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
  
    gender = models.CharField(max_length=1)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(default=None, null=True)
    approved = models.BooleanField(default=False)
    school_id = models.FileField(upload_to='school_ids/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
class School(models.Model):
    name = models.CharField(max_length=100,null=True,blank=False)
    address = models.TextField()
    principal = models.OneToOneField(SchoolAdminProfile, on_delete=models.SET_NULL, null=True, related_name='managed_school')

    
    def __str__(self):
        return self.name

class Standard(models.Model):
    standard_choices = [('1st','1st'),
                        ('2nd','2nd'),
                        ('3rd','3rd'),
                        ('4th','4th'),
                        ('5th','5th'),
                        ('6th','6th'),
                        ('7th','7th'),
                        ('8th','8th'),
                        ('9th','9th'),
                        ('10th','10th'),
                        ('11th','11th'),
                        ('12th','12th'),
                        
                        ]
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,choices=standard_choices,)
    class Meta:
        unique_together = ('school', 'name')  # Prevents duplicate standards per school
    def __str__(self):
        return self.name

class ClassSection(models.Model):
    class_choices = [
        ('A','A'),('B','B'),('C','C'),('D','D')
    ]
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE)
    name = models.CharField(choices=class_choices,max_length=5) 
    class Meta:
        unique_together = ('standard', 'name')
    def __str__(self):
        return f"{self.standard.name} - {self.name}"
    

class Subject(models.Model):
    name = models.CharField(max_length=100)  # Example: "Mathematics", "Science"
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.standard.name})"

class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    # SUBJECT_CHOICES = [('physics','physics'),('maths','maths'),('chemistry','chemistry')]
    SUBJECT_CHOICES = [
        ('p', 'Physics'),
        ('m', 'Maths'),
        ('c', 'Chemistry'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    teacher_id= models.AutoField(primary_key=True)
    # subject = models.CharField(max_length=10,choices=SUBJECT_CHOICES,default='Unknown')
    subject = models.ManyToManyField(Subject)
    standard = models.ManyToManyField(Standard)
    standard_class = models.ManyToManyField(ClassSection)
    # school = models.ForeignKey(School,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='O')  # Use 'O' (Other) as default
    email = models.EmailField()
    raw_password = models.CharField(max_length=20,null=True,blank=True)
    

    def __str__(self):
        return f'{self.name}'

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
    email = models.EmailField(unique=True,max_length=80, default='abc@gmail.com')
    date_of_birth = models.DateField(default='2000-01-01')
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='O')  # Use 'O' (Other) as default
    attendance = models.IntegerField()  # Remove max_length
    subject = models.ManyToManyField(Subject)
    standard = models.ManyToManyField(Standard)
    standard_class = models.ManyToManyField(ClassSection)
    avg_pat_score = models.FloatField(null=True, blank=True)
    avg_sat_score = models.FloatField(null=True, blank=True)
    raw_password = models.CharField(max_length=20, null=True, blank=True)  
    
    # Store the predicted performance
    performance_summary = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_full_name(self):  
        return f"{self.first_name} {self.last_name}"


class Marks(models.Model):
    student = models.ForeignKey(student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
   
    pat_score = models.FloatField(null=True,blank=True)
    sat_score = models.FloatField(null=True,blank=True)

    marks_obtained = models.FloatField(null=True,blank=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    class Meta:
        unique_together = ('student','subject')
   

    @property
    def standard(self):
        return self.subject.standard
    



# messages and chats

class Room(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    participants =models.ManyToManyField(User,related_name='participants',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=131)
    # participants =models.ManyToManyField(User,related_name='participants',blank=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -message"

    class Meta:
        ordering =['-updated','-created']



class StudentSuggestion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description  = models.TextField(max_length=500,null=True,blank=True)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    updated  = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.description[:10]






# SchoolAdmin - > 
    # create teacher and make teacher associates with standard 
    # create standards and standard wise classes so that it can associate to teacher while creating teacher profile by Sca
    #after it was done 

# Teacher - >
    # login via spreadsheet of account id pasword -> teacher login and then 
    # redy standard and class structure which was created by schooladmin is used to add studentdata / creating student profile
    # ex dhrumil is student it was created by teacher and added to standard 4th class/Division A 
    # standards have partucular subjects given by schooladmin 

# Student->
    #can view it's data enterd by teacher and get subject wise sugggesions 

# School Admin creates structure of school which is used by students and Teachers 