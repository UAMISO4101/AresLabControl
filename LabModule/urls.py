from django.conf.urls import url

from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name='home'),
    url(r'^agregarLugar/$', views.agregar_lugar, name='agregarLugar'),
]
