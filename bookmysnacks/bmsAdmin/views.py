from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import Login, Location, User
from partners.models import Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib import messages
from partners.models import Theater
# users/views.py
# from django.contrib.auth.views import LoginView
# from django.urls import reverse

""" Create your views here.
def hello(request):
    w = LOGIN.objects.get(id=1)
    return HttpResponse(f"God, Bless me => {w.username}")
"""



# class UserLoginView(LoginView):
#     template_name = 'bmsAdmin/login.html'
    
#     def get_success_url(self):
#         return self.request.GET.get('next', reverse('home'))

# # Repeat for other apps with their own views


def AdminLog(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Login.objects.get(username=username)
            if user.password == password:
                user.last_login = timezone.now()  # Update last login
                user.save()  # Save the updated user instance
                login(request, user)  # Log the user in
                # return redirect('home')
                return render(request, 'bmsAdmin/home.html')
            else:
                error_message = "Invalid Password"
        except Login.DoesNotExist:
            error_message = "Invalid Username"

    return render(request, 'bmsAdmin/login.html', {'error_message': error_message})



@login_required
def Home(request):
    return render(request, 'bmsAdmin/home.html')


# @login_required
# def adminLogOut(request):
#     logout(request)
#     return render(request, 'bmsAdmin/login.html')

@login_required
def adminLogOut(request):
    print("Logging out user:", request.user)  # Debug statement
    logout(request)
    print("Redirecting to login")  # Debug statement
    return redirect('bmsAdmin:login')

def addCategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryName')
        
        # Basic validation to check if the category name is not empty
        if category_name:
            # Create the category and save it to the database
            Category.objects.create(category_name=category_name)
            messages.success(request, 'Category added successfully!')
            return redirect('bmsAdmin:viewCategory')
        else:
            messages.error(request, 'Category name cannot be empty.')

    return render(request, 'bmsAdmin/home.html', {'active_page': 'addCat'})

def viewAndManageCategory(request):
    categories = Category.objects.all()
    content = {
        'categories': categories,
        'active_page': 'viewCat',
    }
    return render(request, 'bmsAdmin/home.html', content)

def addLocation(request):
    if request.method == 'POST':
        location_name = request.POST.get('LocationName')
        
        if location_name:
            Location.objects.create(location=location_name)
            messages.success(request, 'Location added successfully!')
            return redirect('bmsAdmin:viewLoc')
        else:
            messages.error(request, 'Location name cannot be empty.')
    return render(request, 'bmsAdmin/home.html', {'active_page': 'addLoc'})


def viewAndManageLocation(request):
    locations = Location.objects.all()
    content = {
        'locations': locations,
        'active_page': 'viewLoc',
    }
    return render(request, 'bmsAdmin/home.html', content)


def deleteCategory(request, catId):
    category = get_object_or_404(Category, id=catId)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('bmsAdmin:viewCategory')
    return redirect('bmsAdmin:viewCategory')

def editCategory(request, catId):
    category = get_object_or_404(Category, id=catId)
    
    if request.method == 'POST':
        category_name = request.POST.get('categoryName')
        
        if category_name:  
            category.category_name = category_name
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('bmsAdmin:viewCategory')
        else:
            messages.error(request, 'Category name cannot be empty.')
    
    return render(request, 'bmsAdmin/editCat.html', {'category': category})


def viewUsers(request):
    users_ = User.objects.all()
    user_details = []
    for i in users_:
        userlog = Login.objects.get(id=i.login.id)
        user_details.append({
            'user_id': i.id,
            'username': userlog.username, 
            'fname': i.fname, 
            'lname': i.lname,
            'email': i.email,  
            'phone': i.phone,
            'createdAt': i.created_at
            })
        
    content = {
        'active_page': 'users',
        'user_details': user_details
    }
    return render(request, 'bmsAdmin/home.html', content)

def showTheaters(request):
    theaters = Theater.objects.all()
    content = {
        'active_page': 'theaters',
        'theaters': theaters
    }
    return render(request, 'bmsAdmin/home.html', content)
