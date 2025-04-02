from .views import is_admin,is_student,is_teacher
from student.models import student


def global_context(request):
    user =request.user
    stundent_obj = student.objects.get(user=user)
    
    return {
        'student':stundent_obj,
        'is_student':is_student(request.user),
        'is_teacher':is_teacher(request.user),

    }