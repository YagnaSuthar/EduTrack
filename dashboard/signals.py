from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from student.models import SchoolAdminProfile

@receiver(user_signed_up)
def set_unapproved_status(request, user, **kwargs):
    """Only mark school admins as unapproved"""
    school_admin_group, _ = Group.objects.get_or_create(name='SchoolAdmin')  # Ensure group exists
    if school_admin_group in user.groups.all():
        SchoolAdminProfile.objects.create(user=user, approved=False)
