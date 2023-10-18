from django.urls import path
from .views import index, admin, usuario, cliente, login, registro, medico

urlpatterns = [
    path('', index, name='index'),
    path('admin', admin, name='admin'),
    path('usuario', usuario, name='usuario'),
    path('cliente', cliente, name='cliente'),
    path('login', login, name='login'),
    path('registro', registro, name='registro'),
    path('medico', medico, name='medico')
]


