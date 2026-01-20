from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import signup_view, cars_for_sale, manager_signup_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('', views.car_list, name='car_list'),                      # Read all (internal)
    path('create/', views.car_create, name='car_create'),           # Create
    path('assign/<int:car_id>/', views.assign_car, name='assign_car'),  # Assign car
    path('signup/', signup_view, name='signup'),                    # Signup
    path('signup/manager/', manager_signup_view, name='manager_signup'),
    path('cars/', cars_for_sale, name='cars_for_sale'),             # Public listing
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),# Read one
    path('update/<int:car_id>/', views.car_update, name='car_update'),# Update
    path('delete/<int:car_id>/', views.car_delete, name='car_delete'),# Delete

    # Add this line for logout
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
