from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reservar/', views.reservar_aula, name='reservar_aula'),
    path('reservas-json/', views.reservas_json, name='reservas_json'),

]
