from django.urls import path
from client.views import *

# from django.views.static import serve 
app_name = 'client'

urlpatterns = [
    
    path('client/home', ClientView.as_view(), name="client_home"),

]