from django import forms

class UsuarioForm(forms.Form):
    rut = forms.CharField(max_length=12)
    correo = forms.EmailField()
    nombre = forms.CharField(max_length=100)
    contraseña = forms.CharField(widget=forms.PasswordInput())


class RegistroForm(forms.Form):
    rut = forms.CharField(label="RUT", max_length=10, min_length=10) 
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