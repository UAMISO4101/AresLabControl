# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name = 'home'),
    # Lugar de almacenamiento
    url(r'^agregarLugar/$', views.agregar_lugar, name = 'agregarLugar'),
    url(r'^listaLugares/$', views.listar_lugares, name = 'listaLugares'),
    url(r'^verLugar/(?P<pk>[\w\-]+)/$', views.listar_lugar, name = 'verLugar'),
    # Usuarios
    url(r'accounts/register/$', views.registrar_usuario, name = 'registration_register'),
    # Maquinas
    url(r'^maquina/add/$', views.maquina_create, name = 'maquina-add'),
    url(r'^maquina/$', views.listarMaquinas, name = 'Maquinas-listar'),
    url(r'^maquina/(?P<pk>[\w\-]+)/$', views.maquina_update, name = 'maquina-update'),
    url(r'^reservarMaquina/(?P<pk>[\w\-]+)/$', views.reservar_maquina, name = 'reservarMaquina'),
    # Muestras
    url(r'^solicitarMuestra/$', views.crear_solicitud_muestra, name = 'solicitarMuestra'),
    url(r'^solicitarMuestra/experimentos/$', views.cargar_experimentos, name = 'experimentos'),
    url(r'^solicitarMuestra/protocolos/$', views.cargar_protocolos, name = 'protocolos'),
    url(r'^solicitarMuestra/pasos/$', views.cargar_pasos, name = 'pasos'),
    url(r'^solicitarMaquina/$', views.crear_solicitud_maquina, name = 'solicitarMaquina'),
    # Detalle Muestra
    url(r'^verMuestra/(?P<pk>[\w\-]+)/$', views.listar_muestra, name = 'verMuestra'),
    url(r'^reservarMuestra/$', views.reservar_muestra, name = 'reservarMuestra'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
