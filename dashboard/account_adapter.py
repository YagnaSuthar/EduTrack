from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib import messages

class CustomAccountAdapter(DefaultAccountAdapter):
    def authenticate(self, request, **credentials):
        """Prevent unapproved school admins from logging in"""
        user = super().authenticate(request, **credentials)
        if user:
            school_admin_group = Group.objects.get(name='SchoolAdmin')  # Ensure group exists
            if school_admin_group in user.groups.all():
                # Only check approval for school admins
                if hasattr(user, 'schooladminprofile') and not user.schooladminprofile.approved:
                    messages.error(request, "Your account is pending approval.")
                    # messages.error(request, "Your account is pending approval.")
                    return None
        return user
