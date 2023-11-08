import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from .forms import  RegistroForm, LoginForm, AgregarMedico, agregarDisponibilidad, nuevaHora, fechaHora
# Create your views here.


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






def paciente(request):
    return render(request, "paciente.html")


def tomaHoras(request):
    return render(request, "tomaHoras.html")

def asignarDispo(request, rut):



    form = agregarDisponibilidad()
    form.initial['rut'] = rut
    return render(request, "asignarDisponibilidad.html", {"form" : form})

#RESERVAR HORA

def reservaHora(request):

    if request.method == "POST":

        form = nuevaHora(request.POST)
        if form.is_valid():
            data = {

                'id': form.cleaned_data['especialidad'],

            }


            response = requests.get('https://medicocentro--juaborquez.repl.co/api/disponibilidad/especialidad/', json=data)
            if response.status_code == 200:
                data_esp = response.json()
                messages.success(request, "enviado")
            
                return render(request, "calendario.html", {"data":data_esp})
            else:
                form.add_error(None, "Error al mandar a la API")
    else:
        form = nuevaHora()

    return render(request, "reservaHora.html", {"form": form})


def calendario(request):

    if request.method == "POST":
        form = fechaHora(request.POST)
        

    else: 
        form = fechaHora()

    return render(request, "calendario.html",{"form": form})