from django.urls import path
from . import views

urlpatterns = [
    # path('locations/', views.sitios_interes, name='locations'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('create_train_data/', views.create_train_data, name='create_train_data'), #crear nuevo modelo
    path('train_model/', views.train_model, name='train_model'), #entrenar Modelo
    path('prediction_model/', views.prediction_model, name='prediction_model'), #hacer Prediccion
    path('train_version/<int:train_version_id>/', views.train_version_detail, name='train_version_detail'), #Vista por modelo
]