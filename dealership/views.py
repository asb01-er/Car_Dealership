from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Car, Profile
from .forms import CarForm
from django.shortcuts import render
from .models import Car

@login_required
def home_view(request):
    return render(request, 'home.html')


def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user, role='employee')  # default role
        login(request, user)
        return redirect('car_list')
    return render(request, 'signup.html', {'form': form})

def manager_signup_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user, role='manager')  # Assign manager role
        login(request, user)
        return redirect('car_list')  # Or wherever you want to redirect
    return render(request, 'signup.html', {'form': form})


def is_manager(user):
    return hasattr(user, "profile") and user.profile.role == 'manager'

@login_required
def car_list(request):
    cars = Car.objects.all()
    return render(request, "car_list.html", {"car": cars})

@login_required
@user_passes_test(is_manager)
def car_create(request):
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("car_list")
    return render(request, "car_form.html", {"form": form})

@user_passes_test(is_manager)
def assign_car(request, car_id):
    car= get_object_or_404(Car, id=car_id)
    employees= Profile.objects.filter(role="employee")
    if request.method == 'POST':
        emp_id = request.POST.get("employee")  
        car.assigned_to_id = emp_id
        car.save()
        return redirect("car_list")
    return render(request, "assign_car.html", {'car': car, 'employees': employees})  

@user_passes_test(is_manager)
def car_update(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)

    if form.is_valid():
        form.save()
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
        return redirect('car_list')
    return render(request, 'car_confirm_delete.html', {'car': car})

def cars_for_sale(request):
    cars = Car.objects.filter(for_sale=True)
    return render(request, 'cars_for_sale.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_detail.html', {'car': car})        

