from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS_CHOICES = (
    ("complete", "complete"),
    ("approved", "approved"),
    ("missing info", "overdue"),
    ("archived", "archived")
)

class Material(models.Model):
    material_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    received_qty = models.CharField(max_length=1000)
    PO_qty = models.ForeignKey(User, on_delete=models.CASCADE)
    unit_measure = models.CharField(max_length=2)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Ticket(models.Model):
    ticket_id = models.IntegerField()
    ticketed_at = models.DateTimeField(auto_now_add=True)
    job_id = models.IntegerField(primary_key=True)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=250)
    quantity = models.IntegerField()
    note = models.CharField(max_length=500)
    status = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket_id
    
    class Meta:
        ordering = ['ticketed_at']

class Invoice(models.Model):
    invoice_id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField()
    tickets = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=100)
    invoice_date = models.DateTimeField()
    due_date = models.DateTimeField()
    status = models.DateTimeField()
    amount = models.IntegerField()
    
    def __str__(self):
        return self.invoice_id
    
    class Meta:
        ordering = ['invoice_date']

class Job(models.Model):
    # job_id = models.IntegerField()
    materials = models.ForeignKey(Material, on_delete=models.CASCADE)
    employees = models.ForeignKey(User, on_delete=models.CASCADE)
    # add validation keeping this to only 10 digits
    number = models.CharField(max_length=250)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    owner = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    contract_time = models.IntegerField()
    invoices = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    tickets = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']






