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
            
            if group == "Admin":
                return redirect('pending_requests')
            
            
            # return redirect('/dashboard-home/')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func


# It can able to handle multiple group's user to accesss particular single page (ex SchoolAdmin can acces student list and teacher list both )

GROUP_BASED_HOME_URL = {
    'Admin':'pending_requests',
    'SchoolAdmin':'schooladmin_dash',
    'Teacher':'teacher_dash',
    'Student':'student_dash',

}


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
               redirect_url = GROUP_BASED_HOME_URL.get(group,'/')
               return redirect(redirect_url)
           
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
            
            if group == 'SchoolAdmin':
                return redirect('schooladmin_dash')
            
            if group == 'Admin':
                return redirect('pending_requests')
            
            if request.user.is_superuser:
                return HttpResponse('Even super user cant Access This Admin request page ')

            if group == 'Teacher':
                return view_func(request,*args, **kwargs)
            
            if group =='None':
                return HttpResponse('You have not access to access this page!! ')
            
            
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
        
        if group == "Admin":
            return redirect('pending_requests')
        
        if group == 'Student':
            return  view_func(request,*args, **kwargs)
        
        
        if group == 'None':
            return HttpResponse('You are not authorized to view this page!')

    return wrapper_func


def school_admin_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Teacher':
            return redirect('teacher_dash')

        if group == 'Student':
            return redirect('student_dash')
        
        if group == 'Admin':
            return redirect('pending_requests')

        if group == 'SchoolAdmin':
            return view_func(request,*args, **kwargs)
        
        if group == 'None':
            return HttpResponse('You have not access to access this page !!')
        
    
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        user = request.user

        if user.groups.exists():
            group = user.groups.all()[0].name

        if group == 'Admin':
            return view_func(request,*args, **kwargs)
        
        else:
            return HttpResponse('This is Admin page you cant access this page !!')