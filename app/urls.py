from django.urls import path
from .views import index, admin, tomaHoras, cliente, login, registroUsuario, medico, paciente, deshabilitarCliente, deshabilitarMedico,agregarMedico, tomaHoras, asignarDispo, reservaHora

urlpatterns = [
    path('', index, name='index'),
    path('admin', admin, name='admin'),
    path('cliente', cliente, name='cliente'),
    path('login', login, name='login'),
    path('registro', registroUsuario, name='registro'),
    path('medico', medico, name='medico'),
    path('deshabilitar/<str:rut>/', deshabilitarCliente, name='deshabilitar'),
    path('deshabilitarMedico/<str:rut>/', deshabilitarMedico, name='deshabilitarMedico'),
    path('agregarMedico', agregarMedico, name='agregarMedico'),
    path('tomaHoras', tomaHoras, name='tomaHoras'),
    path('asignarDispo/<str:rut>', asignarDispo, name='asignarDisponibilidad'),
    path("reservaHora", reservaHora, name="reservaHora")
]

