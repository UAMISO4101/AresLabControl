from django.conf.urls import url

from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.home, name='login'),
    url(r'^logout/$', views.home, name='logout'),
    url(r'^register/$', views.home, name='register'),

    # Lugar de almacenamiento
    url(r'^agregarLugar/$', views.agregar_lugar, name='agregarLugar'),
]