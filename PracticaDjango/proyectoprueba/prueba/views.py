from django.shortcuts import render,HttpResponse
from django.urls import reverse
from datetime import datetime
from .forms import ClienteForm

# Create your views here.
def saludo(request):
    return HttpResponse(" Hola les saluda Django")

def info_usuario(request):
    nombre = "Alan Brito"
    edad = 25
    return HttpResponse(f"hola soy {nombre} mi edad {edad}")

def saludo_mejorado(request, nombre, edad):
    return HttpResponse(f"hola soy {nombre} edad {edad}")

def tabla_multiplicacion(request):
    tabla=5
    resultado=""
    for i in range(1,11):
        resultado = resultado+f"{tabla} x {i} = {tabla*i}<br>"
    return HttpResponse(resultado)

def saludo2(request):
    datos={
        'nombre':'Alam Brito',
        'edad':25
    }
    return render(request,'saludo.html', datos)

def info(request):
   return render(request,'informacion.html')

def nuevosaludo(request,nombre, edad):
    return render(request,'nuevosaludo.html',{'nombre':nombre,'edad':edad})

def tabla_producto(request,num):
    lista = []
    for i in range(1, 11):
        res= f"{num} x {i} = {num * i}"
        lista.append(res)
    return render(request, 'tabla_producto.html', {'num': num, 'lista': lista})

def formulario_cliente(request):
    datos= None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        anioNac = request.POST.get('anioNac')
        edad =datetime.now().year - int(anioNac)
        pais = request.POST.get('pais')
        datos={
            'nombre': nombre,
            'correo': correo,
            'anioNac': anioNac,
            'edad': edad,
            'pais': pais
        }
    return render(request,'formulario.html',{'datos':datos})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST) #creando un objeto de la clase clienteForm
        if form.is_valid():
            datos =form.cleaned_data
            return render(request, 'cliente_exito.html', {'datos': datos})
    else:
        inicial={
            'nombre':'',
            'correo':'',
            'anioNac':'',
        }
        form = ClienteForm(initial=inicial)
    return render(request,'cliente_formulario.html',{'form':form})