from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('contact/<int:state>', views.contact, name='contact'),
    path('confirmation/', views.confirmation, name='confirmation_page'),
]
