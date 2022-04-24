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
    
    

]