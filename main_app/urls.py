from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.Home.as_view(), name="home"),

    # Ticket CRUD
    path('tickets/', views.Tickets.as_view(), name = "tickets"),
    path('tickets/new', views.Ticket_Create.as_view(), name = "ticket_create"),
    # path('tickets/<int:pk>', views.Ticket_Detail.as_view(), name = "ticket_detail"),
    # path('tickets/<int:pk>/update', views.Ticket_Update.as_view(), name="ticket_update"),
    # path('tickets/<int:pk>/delete', views.Ticket_Delete.as_view(), name="ticket_delete"),

    # Job CRUD
    path('jobs/', views.Jobs.as_view(), name = "jobs"),
    path('jobs/new', views.Job_Create.as_view(), name = "job_create"),
    path('jobs/<int:pk>', views.Job_Detail.as_view(), name = "job_detail"),
    path('jobs/<int:pk>/update', views.Job_Update.as_view(), name="job_update"),
    # path('jobs/<int:pk>/delete', views.Job_Delete.as_view(), name="job_delete"),

    # Material CRUD
    path('materials/', views.Materials.as_view(), name = "materials"),
    path('jobs/<int:pk>/materials/new', views.Material_Create.as_view(), name = "material_create"),
    # path('materials/<int:pk>', views.Material_Detail.as_view(), name = "material_detail"),
    # path('materials/<int:pk>/update', views.Material_Update.as_view(), name="material_update"),
    # path('materials/<int:pk>/delete', views.Material_Delete.as_view(), name="material_delete"),

    

]