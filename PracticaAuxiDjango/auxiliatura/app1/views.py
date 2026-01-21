from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def home(request):
    raw_links=[
        ('home', 'home', {}),
        ('Ir a saludo', 'saludo', {'nombre':'kevin'}),
        ('Ir a producto', 'producto_detalle', {'pid':24}),
    ]
#dic
    links=[]
    for texto, route, kwargs in raw_links:
        url= reverse(route, kwargs=kwargs)
        links.append({'texto': texto, 'url':url})
    return render(request, 'home.html', {'links':links})
def saludo(request, nombre:str):
    return render(request,'saludo.html', {'nombre':nombre})
def producto_detalle(request, pid:int):
    return render(request,'producto.html',{'pid':pid})
def construir_nombre_completo(nombres:str,paterno:str, materno:str)-> str:
    partes=[nombres.strip(), paterno.strip() , materno.strip()]
    return " ".join(p for p in partes if p)

@csrf_protect
def registro (request):
    contexto={
        'nombres':'',
        'paterno':'',
        'materno':'',
        'fecha_nac':'',
        'ci':'',
        'correo':'',
        'telefono':'',
        'nombre_completo':'',
    }
    if request.method=='POST':
        contexto['nombres']=request.POST.get('nombres','')
        contexto['paterno']=request.POST.get('paterno','')
        contexto['materno']=request.POST.get('materno','')
        contexto['fecha_nac']=request.POST.get('fecha_nac','')
        contexto['ci']=request.POST.get('ci','')
        contexto['correo']=request.POST.get('correo','')
        contexto['telefono']=request.POST.get('telefono','')
        contexto['nombre_completo']=construir_nombre_completo(
            contexto['nombres'],
            contexto['paterno'],
            contexto['materno'],
        )

    return render(request, 'registro.html', contexto)

def registro2(request):
    if request.method=='POST':
        nombres=request.POST.get('nombres','')
        paterno=request.POST.get('paterno','')
        materno=request.POST.get('materno','')
        fecha_nac=request.POST.get('fecha_nac','')
        ci=request.POST.get('ci','')
        correo=request.POST.get('correo','')
        telefono=request.POST.get('telefono','')
        nombre_completo=construir_nombre_completo(nombres, paterno, materno)
        contexto={
            'nombres':nombres,
            'paterno':paterno,
            'materno':materno,
            'fecha_nac': fecha_nac,
            'ci':ci,
            'correo':correo,
            'telefono':telefono,
            'nombre_completo': nombre_completo,
        }
        return render (request, 'registro_resultado.html', contexto)
    
    return render(request, 'registro2.html')
    