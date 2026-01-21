from django.shortcuts import render,redirect, get_object_or_404
from .models import Cliente
from .models import Tienda
from .forms import ClienteForm

# Create your views here.
def listar_clientes(request):
    clientes=Cliente.objects.all()#SELECT * FROM CLIENTES
    return render(request, 'listar_clientes.html', {'clientes':clientes})

def listar_tiendas(request):
    tiendas=Tienda.objects.all()
    return render(request,'listar_tiendas.html',{'tiendas':tiendas})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes') 
    else:
        form = ClienteForm()
        return render(request, 'crear_cliente.html', {'form': form})
    
def modificar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'modificar_cliente.html', {'form': form})
    
def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    cliente.delete()
    return redirect('listar_clientes')