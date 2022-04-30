from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

# Create your models here.

STATUS_CHOICES = (
    ("complete", "complete"),
    ("approved", "approved"),
    ("missing info", "overdue"),
    ("archived", "archived")
)

ROLE_CHOICES = (
    ("Foreman", "Foreman"),
    ("Project Engineer", "Project Engineer"),
    ("Accounting", "Accounting"),
)

class MyUserManager(BaseUserManager): 
    def create_user(self, email, first_name, last_name, phone_number, role, password=None): 
        if not email: 
            raise ValueError("Users must enter an email address")
        if not first_name: 
            raise ValueError("Users must enter a name")
        if not last_name: 
            raise ValueError("Users must enter a last name")
        if not phone_number: 
            raise ValueError("Users must enter a phone number")
        if not role: 
            raise ValueError("Users must choose a role")
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name, 
            last_name = last_name,
            phone_number = phone_number,
            role = role

        )
        user.set_password(make_password(password))
        user.save(using=self._db)
        return user
    
        
    def create_superuser(self, email, first_name, last_name, phone_number, role, password=None): 
        if not email: 
            raise ValueError("Users must enter an email address")
        if not first_name: 
            raise ValueError("Users must enter a name")
        if not last_name: 
            raise ValueError("Users must enter a last name")
        if not phone_number: 
            raise ValueError("Users must enter a phone number")
        if not role: 
            raise ValueError("Users must choose a role")
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            role = "admin",
            is_admin = True, 
            is_staff = True,
            is_superuser = True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser): 
    email = models.EmailField(verbose_name = "email", max_length=250, unique = True) 
    first_name = models.CharField(max_length = 250)
    last_name = models.CharField(max_length = 250)
    role = models.CharField(max_length=20, choices = ROLE_CHOICES)
    objects = MyUserManager()
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'role']

    def __str__(self): 
        return self.first_name + " " + self.last_name
    
    def has_perm(self, perm, obj=None): 
        return self.is_admin

    def has_module_perms(self, app_label): 
        return True

# MUST CREATE INTERMEDIARY MODEL
# If multiple jobs have the same item, their quantities will be the same...

class Job(models.Model):
    # materials = models.ManyToManyField(Material, related_name='material')
    employees = models.ManyToManyField(User, related_name='employee')
    # add validation keeping this to only 10 digits
    number = models.CharField(max_length=250)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    owner = models.CharField(max_length=300)
    start_date = models.DateField()
    contract_time = models.IntegerField()


class Material(models.Model):
    name = models.CharField(max_length=15)
    received_qty = models.CharField(max_length=1000, blank=True)
    PO_qty = models.IntegerField()
    unit_measure = models.CharField(max_length=2)
    cost_code = models.CharField(max_length=25)
    job = models.ForeignKey(Job, related_name='materials', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']



class Ticket(models.Model):
    ticketed_at = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=250)
    quantity = models.IntegerField()
    note = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices = STATUS_CHOICES)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_id
    
    class Meta:
        ordering = ['ticketed_at']

class Invoice(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    tickets = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=100)
    invoice_date = models.DateTimeField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices = STATUS_CHOICES)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.invoice_id
    
    class Meta:
        ordering = ['invoice_date']








