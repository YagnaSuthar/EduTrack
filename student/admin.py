from django.contrib import admin
from .models import student,Teacher,SchoolAdminProfile,School,Subject,Standard,ClassSection
# Register your models here.
admin.site.register(student)
admin.site.register(Teacher)
admin.site.register(SchoolAdminProfile)
admin.site.register(School)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(ClassSection)

