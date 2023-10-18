from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request,'index.html')


def admin(request):
    return render(request, 'admin.html')

def usuario(request):
    return render(request, 'usuario.html')


def cliente(request):
    return render(request, 'cliente.html')


def registro(request):
    return render(request, 'registro.html')

def login(request):
    return render(request, 'login.html')

def medico(request):
    return render(request, 'medico.html')