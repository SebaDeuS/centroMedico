import re
from django import forms
from itertools import cycle
from django.core.exceptions import ValidationError

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

    