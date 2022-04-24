from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Ticket, Job

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - SmartTicket"
        return context

class Tickets(TemplateView):
    template_name = 'tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tickets = Ticket.objects.all()
        context["all_tickets"] = all_tickets
        context["title"] = "Tickets - SmartTicket"
        return context

class Ticket_Create(CreateView):
    template_name = 'ticket_create.html'
    model = Ticket
    fields = ['ticket_id', 'job_id', 'number', 'quantity', 'note', 'status']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.signer = self.request.user
        self.object.save()
        return HttpResponseRedirect('/tickets')



class Jobs(TemplateView):
    template_name = 'jobs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_jobs = Job.objects.all()
        context["all_jobs"] = all_jobs
        context["title"] = "Jobs - SmartTicket"
        return context

class Job_Create(CreateView):
    template_name = 'job_create.html'
    model = Job
    fields = ['number', 'name', 'address', 'owner', 'start_date', 'contract_time']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.employee = self.request.user
        self.object.save()
        return HttpResponseRedirect('/jobs')
