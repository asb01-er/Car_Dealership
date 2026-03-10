from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from .models import Car, Profile
from .forms import CarForm

# -------------------------------
# Helper functions
# -------------------------------
def is_manager(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == 'manager'

# -------------------------------
# Home
# -------------------------------
@login_required
def home_view(request):
    return render(request, 'home.html')

# -------------------------------
# Signup Views
# -------------------------------
def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='employee')  # default role
            login(request, user)
            messages.success(request, "Account created successfully 🎉")
            return redirect('car_list')
        else:
            messages.error(request, "Signup failed. Please check the form.")
    return render(request, 'signup.html', {'form': form})

def manager_signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role='manager')
            login(request, user)
            messages.success(request, "Manager account created successfully ✅")
            return redirect('car_list')
        else:
            messages.error(request, "Signup failed. Please check the form.")
    return render(request, 'signup.html', {'form': form})

# -------------------------------
# Login View
# -------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful 👋")
            return redirect("car_list")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")

# -------------------------------
# Car Views
# -------------------------------
@login_required
def car_list(request):
    cars = Car.objects.all()
    return render(request, "car_list.html", {"cars": cars})

@login_required
@user_passes_test(is_manager)
def car_create(request):
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Car created successfully ✅")
        return redirect("car_list")
    return render(request, "car_form.html", {"form": form})

@user_passes_test(is_manager)
def assign_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    employees = Profile.objects.filter(role="employee")
    if request.method == 'POST':
        emp_id = request.POST.get("employee")  
        car.assigned_to_id = emp_id
        car.save()
        messages.success(request, "Car assigned successfully ✅")
        return redirect("car_list")
    return render(request, "assign_car.html", {'car': car, 'employees': employees})  

@user_passes_test(is_manager)
def car_update(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)

    if form.is_valid():
        form.save()
        messages.success(request, "Car updated successfully ✅")
        return render(request, 'partials/car_item.html', {'car': car})

    if request.META.get('HTTP_HX_REQUEST'):
        return render(request, 'partials/car_form.html', {'form': form, 'car': car})
    else:
        return render(request, 'car_form.html', {'form': form, 'car': car})

@user_passes_test(is_manager)
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        messages.success(request, "Car deleted successfully ✅")
        return HttpResponse("")  # HTMX removes the card
    return HttpResponse(status=405)

# -------------------------------
# Public Views
# -------------------------------
def cars_for_sale(request):
    cars = Car.objects.filter(for_sale=True)
    return render(request, 'cars_for_sale.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})        
