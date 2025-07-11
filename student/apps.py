from django.apps import AppConfig
# from .models import student
class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'

    def ready(self):
        import student.signals
    
    def ready(self):
        from django.contrib.auth.models import Group  # ✅ Import inside the method
        create_groups()

def create_groups():
    """Function to ensure groups exist."""
    from django.contrib.auth.models import Group  # ✅ Import again inside the function

    groups = ['Admin', 'Teacher', 'Student','SchoolAdmin']
    for group in groups:
        Group.objects.get_or_create(name=group)

