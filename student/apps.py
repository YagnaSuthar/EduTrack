from django.apps import AppConfig

class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'

    def ready(self):
        from django.contrib.auth.models import Group  # ✅ Import inside the method
        create_groups()

def create_groups():
    """Function to ensure groups exist."""
    from django.contrib.auth.models import Group  # ✅ Import again inside the function

    groups = ['Admin', 'Teacher', 'Student']
    for group in groups:
        Group.objects.get_or_create(name=group)
