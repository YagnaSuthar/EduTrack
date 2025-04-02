from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        user = request.user
        
        if user.is_authenticated:
            group = None
            if user.groups.exists():
                group = user.groups.get(user=user).name
                print("Working..",group)
            if group == 'Teacher':
                return redirect('teacher_dash')
            
            if group == 'Student':
                return redirect('student_dash')
            
            if group == 'SchoolAdmin':
                return redirect('schooladmin_dash')
            
            # return redirect('/dashboard-home/')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
           user = request.user 
           group = None
           if user.groups.exists():
                group = user.groups.all()[0].name

           if group in allowed_roles:
                return view_func(request,*args, **kwargs)
           else:
               return HttpResponse(f'{user}You are not authorized to view this page ! \n Your Group is {group}')
        return wrapper_func
    return decorator 
    

def teacher_only(view_func):
    def wrapper_function(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group == 'Student':
                return redirect('student_dash')
            
            if group == 'Teacher':
                return view_func(request,*args, **kwargs)
            
            if group == 'schooladmin':
                return redirect('schooladmin_dash')
            
    return wrapper_function


def student_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        group = None 
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Teacher':
            return redirect('teacher_dash')
        
        if group == 'SchoolAdmin':
            return redirect('schooladmin_dash')
        
        if group == 'Student':
            return  view_func(request,*args, **kwargs)
        
        if group == 'None' or 'Admin':
            return HttpResponse('You are not authorized to view this page!')

    return wrapper_func


def school_admin_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'SchoolAdmin':
            return view_func(request,*args, **kwargs)
        
        if group == 'Teacher':
            return redirect('teacher_dash')

        if group == 'Student':
            return redirect('student_dash')
    
    return wrapper_func