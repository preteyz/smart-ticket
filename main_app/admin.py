from django.contrib import admin
from .models import Material, Ticket, Invoice, Job

# Register your models here.
myModels = [Material, Ticket, Invoice, Job]
admin.site.register(myModels)
