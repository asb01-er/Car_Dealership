from django import forms
from .models import Car, Department

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price', 'image', 'for_sale']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
