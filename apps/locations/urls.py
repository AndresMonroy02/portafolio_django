from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.sitios_interes, name='locations'),
]

