from django.shortcuts import render
import requests
# Create your views here.


def index(request):
    return render(request,'index.html')


def admin(request):
    return render(request, 'admin.html')

def usuario(request):
    return render(request, 'usuario.html')


def cliente(request):
    
    r = requests.get("https://centromedico--juaborquez.repl.co/api/usuarios/")
    if r.status_code==200:
        data = r.json()
        print(r)
    else:
        data = None
        print("error")
    return render(request, 'cliente.html', {"data": data})

def registro(request):
    return render(request, 'registro.html')

def login(request):
    return render(request, 'login.html')

def medico(request):
    r = requests.get("https://centromedico--juaborquez.repl.co/api/usuarios/medico")
    if r.status_code==200:
        data = r.json()
        print(r)
    else:
        data = None
        print("error")
    return render(request, 'medico.html', {"data":data})