from django.urls import path
from .views import index, admin, tomaHoras, cliente, login, registroUsuario, medico, paciente, deshabilitarCliente, deshabilitarMedico,agregarMedico, tomaHoras, asignarDispo, listadoDisMedico, deshabilitarDisponibilidad, listadoDisTodos, deshabilitarDisponibilidadTodos, reservaHora, calendario, send_confirmation_email, disponiblidadArchivo, get_disponibilidad, agregar_hora

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
    path('listadoDisMedico/<str:rut>', listadoDisMedico, name='listadoDisMedico'),
    path('deshabilitarDisponibilidad/<int:id>', deshabilitarDisponibilidad, name='deshabilitarDisponibilidad'),
    path('deshabilitarDisponibilidadTodos/<int:id>', deshabilitarDisponibilidadTodos, name='deshabilitarDisponibilidadTodos'),
    path('listadoDisTodos', listadoDisTodos, name="listadoDisTodos"),
    path("reservaHora", reservaHora, name="reservaHora"),
    path("calendario/<int:id>", calendario, name="calendario"),
    path("confirmacionEmail", send_confirmation_email, name="confirmacionEmail"),
    path("disponibilidadArchivo", disponiblidadArchivo, name="disponibilidadArchivo"),
    path("getDisponibilidad/<int:id>/<str:dia>", get_disponibilidad, name="getDisponibilidad"),
    path("agregarHora/<str:drun>/<str:hini>/<str:hter>/<str:dia>", agregar_hora, name="agregarHora"),
]

