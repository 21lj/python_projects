from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import todo

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST['task']
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()
    
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # print(username)
        if len(password) < 3:
            messages.error(request, "Password should be at least 3 characters long")
            return redirect('register')
        eUser = User.objects.filter(username=username)
        if eUser:
            messages.error(request, "Username already exists")
            return redirect('register')
        newUser = User.objects.create_user(username=username, email=email, password=password)
        newUser.save()
        messages.success(request,"Created!!")
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        valUser = authenticate(username=username, password=password)
        if valUser is not None:
            auth_login(request, valUser)
            return redirect('home-page')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'todoapp/login.html', {})

@login_required
def delete(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()
    return redirect('home-page')

@login_required
def update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    if get_todo.status == True:
        get_todo.status = False
    else:
        get_todo.status = True
    get_todo.save()
    return redirect('home-page')

@login_required
def logout_U(request):
    logout(request)
    return redirect('login')