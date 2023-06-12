from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_function


def unallowed_actions(requests):
    def wrapper_function(request, *args, **kwargs):
        error = requests.exceptions.HTTPError
        if  error:
            return render(request, 'notfound.html')
        else:
            return redirect('dashboard')
            

    return wrapper_function


"""
If the decorator is expecting parameters, those parameters will be represented at the top of the nest,
Decorator has the class-based view while the wrapper function has the parameters of the class-based view
"""


def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            role = None
            if request.user.role:
                role = request.user.role
            if role in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return render(request, 'notfound.html')

        return wrapper_function

    return decorator


def manager_only(fn):
    def wrapper_fn(request, *args, **kwargs):
        role = None
        if request.user.is_manager:
            return fn(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page.')
    return wrapper_fn


def director_only(fn):
    def wrapper_fn(request, *args, **kwargs):
        role = None
        if request.user.is_director:
            return fn(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to view this page.')

    return wrapper_fn


def admin_redirect(view_func):
    def wrapper_func(request, *args, **kwargs):
        role = None
        
        if request.user.role:
            role = request.user.role

        if request.user.is_approving_officer:
            return redirect('manager_home')
        
        elif role == 'client':
            return redirect('client_home')

        elif role == 'approving_officer':
            return view_func(request, *args, **kwargs)

    return wrapper_func
