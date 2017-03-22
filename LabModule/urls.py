# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name='home'),
    # Lugar de almacenamiento
    url(r'^agregarLugar/$', views.agregar_lugar, name='agregarLugar'),
    url(r'^listaLugares/$', views.listar_lugares, name='listaLugares'),
    url(r'^maquina/add/$', views.maquina_create, name='maquina-add'),
    url(r'^maquina/$', views.ListarMaquinas, name='maquinas-listar'),
    url(r'^maquina/(?P<pag>\d+)$', views.ListarMaquinas, name='maquinas-listar'),
    url(r'^maquina/(?P<que>\w\-)$', views.ListarMaquinas, name='maquinas-listar'),
    url(r'^maquina/(?P<que>\w\-)/(?P<pag>\d+)$', views.ListarMaquinas, name='maquinas-listar'),
    url(r'^maquina/(?P<pk>[\w\-]+)/$',views.maquina_update, name='maquina-update'),
    url(r'^solicitarMuestra/$', views.crear_solicitud_muestra, name='solicitarMuestra'),
    url(r'^solicitarMuestra/experimentos/$', views.cargar_experimentos, name='experimentos'),
    url(r'^solicitarMuestra/protocolos/$', views.cargar_protocolos, name='protocolos'),
    url(r'^solicitarMuestra/pasos/$', views.cargar_pasos, name='pasos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
