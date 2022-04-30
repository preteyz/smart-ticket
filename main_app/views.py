from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Ticket, Job, Material, User

from django.db.models import Q

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
        owner = self.request.GET.get("owner_filter")
        number = self.request.GET.get("number_filter")
        context["all_jobs"] = all_jobs
        context["title"] = "Jobs - SmartTicket"
        context["owners"] = Job.objects.values_list('owner', flat=True).distinct()
        if owner != None:
                context["all_jobs"] = Job.objects.filter(owner__icontains=owner)#filters owner
        if number != None:
                context["all_jobs"] = Job.objects.filter(number__icontains=number)#filters number

        return context

class Job_Create(CreateView):
    template_name = 'job_create.html'
    model = Job
    fields = ['number', 'name', 'address', 'owner', 'start_date', 'contract_time']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.employee = self.request.user
        print(self.request.user)
        self.object.save()
        return HttpResponseRedirect('/jobs')

class Job_Detail(DetailView):
    model = Job
    template_name = "job_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_object = get_object_or_404(Job, id=self.kwargs['pk'])
        # How do I attach a user from my form to this job?
        employee_add = self.request.GET.get("employee_add")

        # materials accessable thru job
        context['job'] = job_object
        # Pull all users that are assigned to the job
        # context['team'] = User.objects.filter(environment__icontains=) 
        context['company'] = User.objects.all()
        context['header'] = 'Jobsite Detail'
        context['materials'] = Material.objects.filter(Q(job = job_object))
        # if employee_add:

        return context

class Materials(TemplateView):
    template_name = 'jobs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_jobs = Job.objects.all()
        context["job_materials"] = all_jobs
        context["title"] = "Materials - SmartTicket"
        context["header"] = "Materials"
        return context

class Material_Create(CreateView):
    template_name = 'job_create.html'
    model = Material
    fields = ['name','PO_qty', 'unit_measure', 'cost_code']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.job = self.kwargs['pk']
        self.object.job = Job.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        print(self.object)

        return HttpResponseRedirect('/jobs')
