from django import forms

class ClienteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", required=True)
    correo = forms.EmailField(label="Correo", required=True)