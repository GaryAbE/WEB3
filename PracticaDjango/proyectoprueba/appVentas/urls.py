from django.contrib import admin
from django.urls import path
from appVentas import views


urlpatterns = [
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('tiendas/', views.listar_tiendas, name='listar_tiendas'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('eliminar_cliente/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('modificar_cliente/<int:id_cliente>/', views.modificar_cliente, name='modificar_cliente'),
]