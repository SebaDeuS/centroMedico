from django.urls import path
from .views import index, admin, usuario, cliente

urlpatterns = [
    path('', index, name='index'),
    path('admin', admin, name='admin'),
    path('usuario', usuario, name='usuario'),
    path('cliente', cliente, name='cliente')
]


