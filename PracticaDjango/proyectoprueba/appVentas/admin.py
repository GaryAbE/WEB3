from django.contrib import admin
from.models import Cliente, Tienda, Compras
# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombre', 'email')
    search_fields =('nombre', 'email')

@admin.register(Tienda)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_tienda', 'nombre', 'direccion')
    search_fields =('nombre', 'direccion')

@admin.register(Compras)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_compra', 'fecha', 'monto')
    search_fields =('fecha', 'monto')