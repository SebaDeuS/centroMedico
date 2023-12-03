import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from datetime import time
from .forms import  RegistroForm, LoginForm, AgregarMedico, agregarDisponibilidad, nuevaHora, fechaHora, CSVDisponibilidad
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from django.conf import settings
import csv
from datetime import datetime, time, timedelta
import calendar


# Create your views here.

def bloques_de_tiempo(hora_inicial, hora_final, minutos):
    initial_time = datetime.strptime(hora_inicial, '%H:%M:%S').time()
    final_time = datetime.strptime(hora_final, '%H:%M:%S').time()
    
    time_blocks = []
    current_time = initial_time

    while current_time <= final_time:
        time_blocks.append(current_time)
        current_time = (datetime.combine(datetime.min, current_time) + timedelta(minutes=minutos)).time()

    return time_blocks

def fechas_del_mes(anio, mes, dia):
    primer_dia = datetime(anio, mes, 1)

    primer_dia_de_la_semana = primer_dia.weekday()

    offset = (dia - primer_dia_de_la_semana) % 7

    target_date = primer_dia + timedelta(days=offset)

    _, dias_en_mes = calendar.monthrange(anio, mes)

    todas_las_fechas = [target_date + timedelta(days=7 * i) for i in range((dias_en_mes - offset) // 7 + 1)]

    return todas_las_fechas 


def index(request):
    return render(request,'index.html')

def admin(request):
    return render(request, 'admin.html')


def tomaHoras(request):
    return render(request, 'tomaHoras.html')


def cliente(request):
    
    r = requests.get("https://medicocentro--juaborquez.repl.co/api/usuarios/pacientes")
    if r.status_code==200:
        data = r.json()
        print(r)
    else:
        data = None
        print("error")
    return render(request, 'cliente.html', {"data": data})

def deshabilitarCliente(request, rut):

    
    if request.method == "POST":
        data ={
            'run': rut  
        }
        print(rut)
        response = requests.patch("https://medicocentro--juaborquez.repl.co/api/usuarios/deshabilitar", json=data)
        if response.status_code == 200:
                messages.success(request, "Paciente deshabilitado")
                return redirect(to=cliente)
    return render(request, 'cliente.html')

def deshabilitarMedico(request, rut):
    if request.method == "POST":
        data ={
            'run': rut  
        }
        print(rut)
        response = requests.patch("https://medicocentro--juaborquez.repl.co/api/usuarios/deshabilitar", json=data)
        if response.status_code == 200:
                messages.success(request, "Medico deshabilitado")
                return redirect(to=medico)
    return render(request, 'medico.html')


def registroUsuario(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            data = {
                'run': form.cleaned_data['rut'],
                'nombre': form.cleaned_data['nombre'],
                'correo': form.cleaned_data['email'],
                'contrasena': form.cleaned_data['password'],
                'tipo_usuario' : 3,
            }
        

            response = requests.post('https://medicocentro--juaborquez.repl.co/api/usuarios/add/', json=data)

            if response.status_code == 200:
                messages.success(request, "Te haz registrado correctamente")
                return redirect(to=index)
            else:
                form.add_error(None, "Error al registrar el usuario en la API")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})




def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'contrasena': form.cleaned_data['password'],
            }
            print(data)
            response = requests.get('https://medicocentro--juaborquez.repl.co/api/usuarios/login/', json=data)
            print(requests.get('https://medicocentro--juaborquez.repl.co/api/usuarios/login/', json=data))

            if response.status_code == 200:
                respuesta = response.json()
                print(respuesta)
                if respuesta.get("msg"):
                    messages.success(request, 'Te haz logeado correctamente')
                    return redirect(to=index)
                else:
                    messages.error(request, 'Correo o contraseña incorrecta')
            else:
                form.add_error(None, "Correo electrónico o contraseña incorrectos. Por favor, inténtalo de nuevo.")
        else:
            form.add_error(None, "Por favor, corrige los errores en el formulario.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})



def medico(request):
    r = requests.get("https://medicocentro--juaborquez.repl.co/api/usuarios/medicos")
    if r.status_code==200:
        data = r.json()
        print(r)
    else:
        data = None
        print("error")

    return render(request, 'medico.html', {"data":data})



def paciente(request):
    return render(request,'paciente.html')

def agregarMedico(request):
    if request.method == "POST":
        form = AgregarMedico(request.POST)
        if form.is_valid():
            data = {
                'run': form.cleaned_data['rut'].lower(),
                'nombre': form.cleaned_data['nombre'],
                'especialidad': form.cleaned_data['especialidad'],
                'correo': form.cleaned_data['email'],
                'contrasena': form.cleaned_data['password'],
                'tipo_usuario' : 1,
            }
        

            response = requests.post('https://medicocentro--juaborquez.repl.co/api/usuarios/add/medico/', json=data)

            if response.status_code == 200:
                messages.success(request, "medico agregado correctamente")
                #Envia una respuesta vacia para evitar que la vista se renderice en el modal y refresca la pagina
                return HttpResponse(status=204, headers={'HX-refresh': 'true'})
            else:
                form.add_error(None, "Error al registrar el usuario en la API")
    else:
        form = AgregarMedico()

    return render(request, "agregarMedicoForm.html", {"form": form})


def disponiblidadArchivo(request):
    if request.method == "POST":
        form = CSVDisponibilidad(request.POST, request.FILES)
        print(request)
        if form.is_valid():
            archivo = request.FILES['csv_file']
            decoded_file = archivo.read().decode('utf-8').splitlines()

            #TODO: Verificar que el "header" tiene el formato adecuado para saltarlo
            csv_header = csv.reader(decoded_file)
            header = next(csv_header, None)

            for row in csv_header:
                run_medico, dia_semana, hora_inicio, hora_termino, tiempo_por_consulta_min = row

                data = {"run_medico":run_medico, "dia_semana": dia_semana, "hora_inicio": hora_inicio, "hora_termino": hora_termino,"tiempo_por_consulta_min": tiempo_por_consulta_min}

                response = requests.post('https://medicocentro--juaborquez.repl.co/api/disponibilidad/add/', json=data)

                if response.status_code != 200:
                    messages.success(request, "Error al agregar la disponibilidad")
                    return HttpResponse(status=204, headers={'HX-refresh': 'true'})
            return HttpResponse(status=204, headers={'HX-refresh': 'true'})
        else:
            print(form.errors)
    else:
        form = CSVDisponibilidad()

    return render(request, "disponibilidad.html", {"form": form})


def paciente(request):
    return render(request, "paciente.html")


def tomaHoras(request):
    return render(request, "tomaHoras.html")



def asignarDispo(request, rut):
    if request.method == "POST":
        form = agregarDisponibilidad(request.POST)
        form.initial['rut'] = rut

        if form.is_valid():
            hora_inicio_cadena = form.cleaned_data['hora_inicio'].strftime('%H:%M')
            hora_termino_cadena = form.cleaned_data['hora_termino'].strftime('%H:%M')
            data = {
                'run_medico' : form.cleaned_data['rut'],
                'dia_semana' : form.cleaned_data['dia'],
                'hora_inicio' : hora_inicio_cadena,
                'hora_termino' : hora_termino_cadena,
                'estado' : True,
                'tiempo_por_consulta_min' : form.cleaned_data['tiempo_consulta'],
            }

            response = requests.post('https://medicocentro--juaborquez.repl.co/api/disponibilidad/add/', json=data)
            
            if response.status_code == 200:
                messages.success(request, "Disponibilidad agregada correctamente")
                
                return redirect(to=medico)
            else:
                form.add_error(None, "Error al agregar disponibilidad en la API")
        
    else:
        form = agregarDisponibilidad()
    return render(request, "asignarDisponibilidad.html", {"form" : form})



def listadoDisMedico(request, rut):
    data ={
            'run': rut  
        }
    r = requests.get("https://medicocentro--juaborquez.repl.co/api/disponibilidad/medico/", json=data)
    if r.status_code==200:
        data = r.json()
        print(r)
    else:
        data = None
        print("error")
    return render(request, "listadoDisMedico.html", {"data":data})



def deshabilitarDisponibilidad(request, id):
    if request.method == "POST":
        data ={
            'disp_id': id
        }
        response = requests.patch("https://medicocentro--juaborquez.repl.co/api/disponibilidad/deshabilitar/", json=data)
        if response.status_code == 200:
                messages.success(request, "Disponibilidad deshabilitada")
                return redirect(to=medico)
    return render(request, 'listadoDisMedico.html')


def deshabilitarDisponibilidadTodos(request, id):
    if request.method == "POST":
        data ={
            'disp_id': id
        }
        response = requests.patch("https://medicocentro--juaborquez.repl.co/api/disponibilidad/deshabilitar/", json=data)
        if response.status_code == 200:
                messages.success(request, "Disponibilidad deshabilitada")
                return redirect(to=listadoDisTodos)
    return render(request, 'listadoDisMedico.html')

def listadoDisTodos(request):
    r = requests.get("https://medicocentro--juaborquez.repl.co/api/disponibilidad/")
    if r.status_code==200:
        data = r.json()
        print(r)
    else:
        data = None
        print("error")
    return render(request, "listadoDisTodos.html", {"data":data})



def reservaHora(request):

    if request.method == "POST":

        form = nuevaHora(request.POST)
        if form.is_valid():
            id = form.cleaned_data['especialidad'],
            print(id)
            return redirect(f'calendario/{id[0]}')
        else:
            form.add_error(None, "Error al mandar a la API")
    else:
        form = nuevaHora()

    return render(request, "reservaHora.html", {"form": form})



def calendario(request, id):
    anio_actual = datetime.now().year
    mes_actual = datetime.now().month
    #Disponibilidad de los medicos con especialidad seleccionada en "reservarHora"
    response = requests.get('https://medicocentro--juaborquez.repl.co/api/disponibilidad/especialidad/', json={"id":id})
    if response.status_code == 200:
        dispo_esp = response.json()
    else:
        messages.success(request, "No se consiguió recuperar las disponibilidades")
    
    #API de feriados
    url_feriados = f'https://apis.digital.gob.cl/fl/feriados/{anio_actual}/{mes_actual}' 
    try:
        responseFeriados = requests.get(url_feriados, headers={'Content-Type': 'application/json', 'Accept': 'text/plain', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',}, verify=True)
        feriados = responseFeriados.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    feriados_fecha= {item['fecha'] for item in feriados}
    feriados_disable = list(feriados_fecha)
    feriados_iso= [f"{dt}T00:00:00" for dt in feriados_disable]


    # Fechas con disponibilidad
    # TODO:No mostrar dias con disponibilidad ocupada
    fechas_iso = []

    dias_unicos = {item['dia_semana'] for item in dispo_esp}
    dias_unicos = list(dias_unicos)
    #Diccionario para usar el calendario y habilitar los dias
    dias_numero = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "domingo": 6,
    }

    for dia in dias_unicos:
        filtro = 'lunes martes miercoles jueves viernes sabado'
        dia_minus = (dia).lower()
        if dia_minus in filtro:
            dia_input = dias_numero[dia_minus]
            fechas = fechas_del_mes(2023,12, dia_input)
            fechas_iso.extend([dt.isoformat() for dt in fechas])

    # Remueve los feriados de las fechas disponibles
    for feriado in feriados_iso:
        if feriado in fechas_iso:
            fechas_iso.remove(feriado)

    if request.method == "POST":
        print(request)

    return render(request, "calendario.html",{"data": dispo_esp, "fechas": fechas_iso, "feriados": feriados_disable, "id":id})

#Email
def send_confirmation_email(request):
    confirmation_link = "https://guthib.com/"

    html_message = render_to_string('confirmacion_email.html', {'confirmation_link': confirmation_link})
    plain_message = strip_tags(html_message)

    send_mail(
        'Confirma tu hora',
        plain_message,
        'settings.EMAIL_HOST_USER',
        ['juanborquez.3@gmail.com'],
        html_message=html_message,
    )

    # Redirect or render a response as needed
    return render(request, 'confirmacion_email.html')

#Tabla de disponibilidad
def get_disponibilidad(request,id,dia):
    filas_horas = []

    response = requests.get('https://medicocentro--juaborquez.repl.co/api/disponibilidad/especialidad/dia', json={"id":id, "dia":dia})
    r = response.json()

    #TODO: Hacer los bloques de hora
    for disp in r:
        bloques = bloques_de_tiempo(disp['hora_inicio'], disp['hora_termino'], disp['tiempo_por_consulta_min'])
        bloques_iso = [dt.isoformat() for dt in bloques]
        horas = []
        for hora in bloques_iso:
            #TODO:Cambiar dia por fecha completa
            horas.append({"hora_inicio":hora})
        medico_horas = {"medico":disp["run_medico"],"disponibilidad":horas}
        filas_horas.append(medico_horas)
    print(filas_horas)

    #Formato de como se deberia enviar la informacion a la tabla hora
    #{"paciente_run":"20913053-3", "doctor_run":disp["run_medico"], "hora_inicio":disp["hora_inicio"], "hora_termino":disp["hora_termino"],"fecha":dia,}

    html_fragment = render_to_string('dispo_table_fragment.html',{'info':filas_horas})
    return HttpResponse(html_fragment)

#def agregar_hora(request,drun,hini,hter,dia):
    #response = requests.post('https://medicocentro--juaborquez.repl.co/api/hora/add', json={'paciente_run':"2091305-3", "doctor_run":drun, "hora_inicio":hini, "hora_termino": hter, "fecha":dia, "estado_hora":1})
    #print(response)