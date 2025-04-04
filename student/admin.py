from django.contrib import admin
from .models import student,Teacher,SchoolAdminProfile
# Register your models here.
admin.site.register(student)
admin.site.register(Teacher)
admin.site.register(SchoolAdminProfile)
