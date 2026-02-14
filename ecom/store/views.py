from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q

# Create your views here.
def search(request):
    # Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched)| Q(description__icontains=searched))
        #Test for nill
        if not searched:
            messages.success(request,'The Product Does not Exist...Please try again!')
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'searched':searched})
    else:
        return render(request,'search.html',{})


def update_info(request):
    if request.user.is_authenticated:
        # Get or create profile
        current_user, created = Profile.objects.get_or_create(user=request.user)
        
        # Debug: Always show a message to test
        # messages.info(request, f"DEBUG - Created: {created}, User: {request.user.username}")
        
        if created:
            name = request.user.first_name or request.user.username
            # Capitalize first letter
            name = name.capitalize()
            messages.success(request, f"🎉 Welcome, {name}! Your profile has been created. Please complete your information below.")
        else:
            # Show a message even if profile already exists
            name = request.user.first_name or request.user.username
            name = name.capitalize()
            messages.info(request, f"👋 Welcome back, {name}! You can update your profile information below.")
        
        # Handle form
        if request.method == "POST":
            form = UserInfoForm(request.POST, instance=current_user)
            if form.is_valid():
                form.save()
                messages.success(request, '✅ Your profile has been updated successfully!')
                return redirect('home')
            else:
                # Show form errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = UserInfoForm(instance=current_user)
        
        # Pass form as 'form' to match template
        return render(request, "update_info.html", {'form': form})
    else:
        messages.error(request, "🔒 You must be logged in to access this page")
        return redirect('home')
    
'''
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id = request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user) 
    
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Info Has Been Updated!!!')
            return redirect('home')
        return render(request, "update_info.html",{'user_form':form})
    else:
        messages.success(request,"You Must be logged in to access this page")
        return redirect('home')
'''    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            #Do Stuff
            form = ChangePasswordForm(current_user,request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request,'Your password has been updated')
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)    
            return render(request, "update_password.html",{'form':form})
    else:
        messages.success(request,'You must be logged in to view this page')
        return redirect('home')    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user) 
    
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'User Has Been Updated!!!')
            return redirect('home')
        return render(request, "update_user.html",{'user_form':user_form})
    else:
        messages.success(request,"You Must be logged in to access this page")
        return redirect('home')

def category(request,foo):
    # Replaces hyphens with Spaces
    foo = foo.replace('-',' ')
    # Grab the category from the url
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products, 'category':category})
    except:  
        messages.success(request,("That Category doesn't exist"))  
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{"categories":categories})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("Login Successful"))
            return redirect('home')
        else:
            messages.success(request,("There was an error,please try again!"))
    else:    
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been Logged Out Successfully!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            # Save the user
            user = form.save()
            
            # Create Profile for the user
            Profile.objects.create(user=user)

            # Log them in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "🎉 You have been Registered Successfully!")
                return redirect('update_info')
        else:
            # Form is invalid - show errors
            messages.error(request, " Please correct the errors below:")
            # Return form with errors
            return render(request, 'register.html', {'form': form})
    
    # GET request - show empty form
    return render(request, 'register.html', {'form': form})