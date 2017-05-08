
from django.shortcuts import render, redirect
from .models import User
from datetime import datetime
from django.contrib import messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'login_registration/index.html')

def validate(request):
    if request.method == 'POST':
        error_flag = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if len(first_name) < 2:
            messages.add_message(request, messages.ERROR,
            'First Name must be at least 2 letters long.')
            error_flag = True
        if not re.match(r'^[A-z]+$', first_name):
            messages.add_message(request, messages.ERROR,
            'First Name can only consist of letters.')
            error_flag = True
        if len(last_name) < 2:
            messages.add_message(request, messages.ERROR,
            'Last Name must be at least 2 letters long.')
            error_flag = True
        if not re.match(r'^[A-z]+$', last_name):
            messages.add_message(request, messages.ERROR,
            'Last Name can only consist of letters.')
            error_flag = True
        if len(email) < 1:
            messages.add_message(request, messages.ERROR,
            'Email cannot be blank.')
            error_flag = True
        elif not re.match(EMAIL_REGEX, email):
            messages.add_message(request, messages.ERROR,
            'Email must be in the correct format.')
            error_flag = True
        if len(password) < 8:
            messages.add_message(request, messages.ERROR,
            'Password must be at least 8 characters.')
            error_flag = True
        if not password == password_confirm:
            messages.add_message(request, messages.ERROR,
            'Passwords must match.')
            error_flag = True
        if error_flag == True:
            return redirect('login_registration:index')
        else:
            user = User.objects.register_user(request.POST)
            request.session['id'] = user.id
            request.session['action'] = 'register'
            return redirect('/success')
    else:
        return redirect('login_registration:index')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not re.match(EMAIL_REGEX, email):
            messages.add_message(request, messages.ERROR,
            'Email must be in the correct format.')
            return redirect('login_registration:index')
        password = request.POST.get('password')
        request.session['action'] = 'login'
        try:
            user = User.objects.get(email=email)
        except:
            messages.add_message(request, messages.ERROR,
            'User does not exist.')
            return redirect('login_registration:index')
        hashed = user.password
        if bcrypt.hashpw(str(password), str(hashed)) == hashed:
            request.session['id'] = user.id
            return redirect('login_registration:success')
        else:
            messages.add_message(request, messages.ERROR,
            'Password is incorrect.')
            return redirect('login_registration:index')
    else:
        return redirect('login_registration:index')

def success(request):
    context = {
        'name': User.objects.get(id=request.session['id']).first_name
    }
    print User.objects.all()
    return render(request, 'login_registration/success.html', context)
