from django import forms #importando la clase form

class ClienteForm(forms.Form):
    nombre= forms.CharField(label='nombre',required=True)
    correo = forms.EmailField(label='correo',required=True)
    anioNac = forms.IntegerField(label='anioNac',required=True)