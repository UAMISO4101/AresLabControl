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
    url(r'^solicitarMuestra/$', views.make_sample_request, name='solicitarMuestra'),
    url(r'^solicitarMuestra/experiments/$', views.get_experiments, name='experiments'),
    url(r'^solicitarMuestra/protocols/$', views.get_protocols, name='protocols'),
    url(r'^solicitarMuestra/steps/$', views.get_steps, name='steps'),
]