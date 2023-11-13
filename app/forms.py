import re
from django import forms
from itertools import cycle
from django.core.exceptions import ValidationError
import requests

def validar_rut(rut):
  rut = rut.upper();
  rut = rut.replace("-","")
  rut = rut.replace(".","")
  aux = rut[:-1]
  dv = rut[-1:]
  
  revertido = map(int, reversed(str(aux)))

  factors = cycle(range(2,8))

  s = sum(d * f for d, f in zip(revertido,factors))

  res = (-s)%11
  if str(res) == dv:
    return True
  elif dv=="K" and res==10:
    return True
  else:
    raise ValidationError("Rut invalido (ejemplo: 12345678-9)")

class UsuarioForm(forms.Form):
    rut = forms.CharField(max_length=12)
    correo = forms.EmailField()
    nombre = forms.CharField(max_length=100)
    contraseña = forms.CharField(widget=forms.PasswordInput())

'''
def validar_rut_chileno(value):
    rut_pattern = r'^\d{7,8}-[\dkK]$'

    if not re.match(rut_pattern, value):
        raise forms.ValidationError("Ingresa un RUT chileno válido (ejemplo: 12345678-9).")

'''

class RegistroForm(forms.Form):
    rut = forms.CharField(label="RUT", max_length=10, min_length=9, validators=[validar_rut]) 
    nombre = forms.CharField(label="Nombre")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    repeat_password = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            self.add_error("repeat_password", "Las contraseñas no coinciden.")


class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())


class AgregarMedico(forms.Form):
    rut = forms.CharField(label="RUT", max_length=10, min_length=9, validators=[validar_rut]) 
    nombre = forms.CharField(label="Nombre")
    especialidad = forms.ChoiceField(label="Especialidad", choices=[])
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    repeat_password = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput())



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            self.add_error("repeat_password", "Las contraseñas no coinciden.")


    def __init__(self, *args, **kwargs):
        super(AgregarMedico, self).__init__(*args, **kwargs)

        api_url = 'https://medicocentro--juaborquez.repl.co/api/especialidad/'

        r = requests.get(api_url)

        if r.status_code == 200:
            data = r.json()
            self.fields['especialidad'].choices = [(especialidad['esp_id'], especialidad['nom_esp']) for especialidad in data] 
        else:
            self.fields['especialidad'].choices = [('', 'error al recuperar la data')] 
    



class agregarDisponibilidad(forms.Form):
    rut = forms.CharField(label="RUT", max_length=10, min_length=9, validators=[validar_rut], widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu RUT'}))
    dia = forms.ChoiceField(label="Día", choices=[], widget=forms.Select(attrs={'placeholder': 'Selecciona un día'}))
    hora_inicio = forms.TimeField(label="Hora de Inicio", widget=forms.TimeInput(attrs={'placeholder': '00:00'}))
    hora_termino = forms.TimeField(label="Hora de Término", widget=forms.TimeInput(attrs={'placeholder': '00:00'}))
    tiempo_consulta = forms.IntegerField(label="Tiempo Consulta", widget=forms.TextInput(attrs={'placeholder': '10'}))

    def __init__(self, *args, **kwargs):
        super(agregarDisponibilidad, self).__init__(*args, **kwargs)
        self.fields['dia'].choices = self.get_dias()
        self.fields['rut'].disabled = True

    def get_dias(self):
        dias = [
            ('Lunes', 'Lunes'),
            ('Martes', 'Martes'),
            ('Miercoles', 'Miércoles'),
            ('Jueves', 'Jueves'),
            ('Viernes', 'Viernes'),
            ('Sabado', 'Sábado')
        ]
        return dias
    

class nuevaHora(forms.Form):
    especialidad = forms.ChoiceField(label = "Especialidad", choices=[], widget= forms.Select(attrs={'placeholder': 'Selecciona una especialidad'}))
    
    
    def __init__(self, *args, **kwargs):

        super(nuevaHora, self).__init__(*args, **kwargs)

        api_url = 'https://medicocentro--juaborquez.repl.co/api/especialidad/'

        r = requests.get(api_url)

        if r.status_code == 200:
            data = r.json()
            self.fields['especialidad'].choices = [(especialidad['esp_id'], especialidad['nom_esp']) for especialidad in data] 
        else:
            self.fields['especialidad'].choices = [('', 'error al recuperar la data')] 

class fechaHora(forms.Form):

    date = forms.DateField( widget= forms.TextInput(attrs = {'class' : 'datepicker'}))
