from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('saludo/<str:nombre>/', views.saludo, name='saludo'),
    path('producto/<int:pid>/', views.producto_detalle, name='producto_detalle'),
    path('registro/', views.registro, name='registro'),
    path('registro2/', views.registro2, name='registro2'),
]