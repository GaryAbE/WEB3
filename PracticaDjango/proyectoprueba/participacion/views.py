from django.shortcuts import render
# Create your views here.
def grupoform(request):
    registro= None
    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        nombreJ = request.POST.get('nombreJ')
        membresia= request.POST.get('membresia')
        cantidad=request.POST.get('cantidad')
        registro={
            'grupo': grupo,
            'nombreJ': nombreJ,
            'membresia': membresia,
            'cantidad': cantidad,
        }
    return render(request,'impar.html',{'registro':registro})
