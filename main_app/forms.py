from django import forms 
from .models import Material
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate
from .models import Material, Ticket, Job
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

class Ticket_Form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('job', 'material_id', 'number', 'quantity', 'note', 'status')
        widgets = {
            'job': forms.Select(attrs={'id':'choicewa'}),
            'material_id': forms.Select(attrs={'id':'choicewa'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            # 'quantity': forms.IntegerField(),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'id':'choicewa'}),
        }

class Ticket_Creation_Form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('job', 'material_id', 'number', 'quantity', 'note', 'status')
        widgets = {
            # populate choice with below
            # 'job': forms.TextInput(attrs={'class': 'form-control'}),
            # 'material_id': forms.TextInput(attrs={'class': 'form-control'}),
            # 'number': forms.TextInput(attrs={'class': 'form-control'}),
            # 'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            # 'note': forms.Textarea(attrs={'class': 'form-control'}),
            # 'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material_id'].queryset = Material.objects.none()

        if 'job' in self.data:
            try:
                job_id = int(self.data.get('job'))
                self.fields['job'].queryset = Job.objects.filter(job_id=job_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['material'].queryset = self.instance.job.material_set.order_by('name')