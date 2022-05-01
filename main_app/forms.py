from django import forms 
from .models import Material
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from .models import Material, User
from django.contrib.auth.hashers import make_password

class Material_Form(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('name','PO_qty', 'unit_measure', 'cost_code')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'PO_qty': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_measure': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_code': forms.TextInput(attrs={'class': 'form-control'}),
        }
    