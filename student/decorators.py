def only_teacher(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.groups.exists(name='Teacher'):
            return view_func
        elif request.user.groups.exists(name='Admin'):
            return  