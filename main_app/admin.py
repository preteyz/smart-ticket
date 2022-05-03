from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Material, Ticket, Invoice, Job

# Register your models here.
# class UsrAdmin(UserAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'role', 'is_admin', 'is_staff')
#     search_fields = ('email', 'username')
#     readonly_fields = ('id')

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

myModels = [Material, Ticket, Invoice, Job]
admin.site.register(myModels)
