from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

import LabModule.app_views.Almacenamiento
import LabModule.app_views.Experimento
import LabModule.app_views.Home
import LabModule.app_views.Maquina
import LabModule.app_views.Muestra
import LabModule.app_views.Paso
import LabModule.app_views.Protocolo
import LabModule.app_views.Solicitud
import LabModule.app_views.Usuario

urlpatterns = [
    # Peticiones a vistas
    url(r'^$',
        LabModule.app_views.Home.home,
        name = 'home'),

    # Lugar de almacenamiento
    url(r'^almacenamiento/add/$',
        LabModule.app_views.Almacenamiento.lugar_add,
        name = 'lugar-add'),

    url(r'^almacenamiento/update/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Almacenamiento.lugar_update,
        name = 'lugar-update'),

    url(r'^almacenamiento/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Almacenamiento.lugar_detail,
        name = 'lugar-detail'),

    url(r'^almacenamiento/$',
        LabModule.app_views.Almacenamiento.lugar_list,
        name = 'lugar-list'),

    # Usuarios
    url(r'accounts/register/$',
        LabModule.app_views.Usuario.registrar_usuario,
        name = 'registration_register'),

    # Maquinas
    url(r'^maquina/add/$',
        LabModule.app_views.Maquina.maquina_add,
        name = 'maquina-add'),

    url(r'^maquina/$',
        LabModule.app_views.Maquina.maquina_list,
        name = 'maquina-list'),

    url(r'^maquina/solicitar/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Maquina.maquina_request,
        name = 'maquina-request'),

    url(r'^maquina/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Maquina.maquina_detail,
        name = 'maquina-detail'),

    url(r'^maquina/update/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Maquina.maquina_update,
        name = 'maquina-update'),

    # Muestras
    url(r'^muestra/$',
        LabModule.app_views.Muestra.muestra_list,
        name = 'muestra-list'),

    url(r'^muestra/solicitar/$',
        LabModule.app_views.Muestra.muestra_request,
        name = 'muestra-request'),

    url(r'^muestra/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Muestra.muestra_detail,
        name = 'muestra-detail'),

    # Servicios

    url(r'^maquina/events/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Solicitud.maquina_reservations,
        name = 's-maquina-reservations'),

    url(r'^solicitarMuestra/experimentos/$',
        LabModule.app_views.Experimento.cargar_experimentos,
        name = 's-experimentos-list'),

    url(r'^solicitarMuestra/protocolos/$',
        LabModule.app_views.Protocolo.cargar_protocolos,
        name = 's-protocolos-list'),

    url(r'^solicitarMuestra/pasos/$',
        LabModule.app_views.Paso.cargar_pasos,
        name = 's-pasos-list'),

    # Solicitudes
    url(r'^aprobarSolicitudMuestras/listar/$',
        LabModule.app_views.Solicitud.listar_solicitud_muestra,
        name = 'solicitudes-muestra-list'),

    url(r'^aprobarSolicitudMuestras/aprobar/$',
        LabModule.app_views.Solicitud.aprobar_solicitud_muestra,
        name = 'solicitud-muestra-aprobar'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
