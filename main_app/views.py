from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import Material_Form, Ticket_Form, Ticket_Creation_Form
from django.views.generic import DetailView
from .models import Ticket, Job, Material, User
from django.urls import reverse, reverse_lazy
from django.db.models import Q

# Auth imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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

@method_decorator(login_required, name='dispatch')
class Ticket_Create(CreateView):
    template_name = 'ticket_create.html'
    model = Ticket
    # form_class = Ticket_Creation_Form
    form_class = Ticket_Form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.signer = self.request.user
        self.object.save()
        self.object.material_id.rcv_material(int(self.object.quantity))
        self.object.material_id.save()
        return HttpResponseRedirect('/tickets')

class Ticket_Detail(DetailView):
    model = Job
    template_name = "ticket_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_object = get_object_or_404(Job, id=self.kwargs['pk'])
        context['job'] = job_object
        context['header'] = 'Ticket Detail'
        # if employee_add:

        return context

# AJAX testing dynamic dropdown
def load_materials(request):
    job_id = request.GET.get('job_id')
    materials = Material.objects.filter(job_id=job_id).all()
    # return render(request, 'material_dropdown_list_options.html', {'materials': materials})
    print(list(materials.values('id', 'name')))
    return JsonResponse(list(materials.values('id', 'name')), safe=False)

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

@method_decorator(login_required, name='dispatch')
class Job_Update(UpdateView):
    template_name = 'job_create.html'
    model = Job
    fields = ['number', 'name', 'address', 'owner', 'start_date', 'contract_time']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.employee = get_object_or_404(Job, id=self.kwargs[self.request.user.pk])
        self.object.save()
        return reverse('location_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class Job_Create(CreateView):
    template_name = 'job_create.html'
    model = Job
    fields = ['number', 'name', 'address', 'owner', 'start_date', 'contract_time']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.employees.add(get_object_or_404(User, id=self.request.user.pk))
        return HttpResponseRedirect('/jobs')

class Job_Detail(DetailView):
    model = Job
    template_name = "job_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_object = get_object_or_404(Job, id=self.kwargs['pk'])
        # How do I attach a user from my form to this job?
        employee_add = self.request.GET.get("employee_add")
        employee_remove = self.request.GET.get("employee_remove")
        # add and remove throwing error
        if employee_add:
            job_object.employees.add(get_object_or_404(User, username=employee_add)) 
            
        # materials accessable thru job
        context['job'] = job_object
        # Pull all users that are assigned to the job
        context['add_employees'] = User.objects.all()
        context['remove_employees'] = job_object.employees.all()
        context['header'] = 'Jobsite Detail'
        context['materials'] = Material.objects.filter(Q(job = job_object))
        # if employee_add:

        return context

@method_decorator(login_required, name='dispatch')
class Job_Delete(DeleteView):
    model = Job
    template_name = "job_confirm_delete.html"
    success_url = "/jobs/"

class Materials(TemplateView):
    template_name = 'jobs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_jobs = Job.objects.all()
        context["job_materials"] = all_jobs
        context["title"] = "Materials - SmartTicket"
        context["header"] = "Materials"
        return context

@method_decorator(login_required, name='dispatch')
class Material_Create(CreateView):
    template_name = 'material_create.html'
    model = Material
    form_class = Material_Form
    success_url = reverse_lazy('jobs')

    def form_valid(self, form):
        form.instance.job = get_object_or_404(Job, id=self.kwargs['pk'])
        form.instance.received_qty = 0
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class Material_Delete(DeleteView):
    model = Job
    template_name = "material_confirm_delete.html"
    success_url = "/jobs/"

def login_view(request):
    # if POST, then authenticate the user (submitting the username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html', {'form': form})
            else:
                return render(request, 'login.html', {'form': form})
        else: 
            return render(request, 'signup.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('Hey', user.username)
            return HttpResponseRedirect('/')
        else:
            HttpResponse('<h1>Try again...</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})