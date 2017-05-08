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

    url(r'^almacenamiento/$',
        LabModule.app_views.Almacenamiento.lugar_list,
        name = 'lugar-list'),

    url(r'^almacenamiento/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Almacenamiento.lugar_detail,
        name = 'lugar-detail'),

    url(r'^almacenamiento/update/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Almacenamiento.lugar_update,
        name = 'lugar-update'),

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
    # url(r'^muestra/add/$',
    #     LabModule.app_views.Muestra.muestra_add,
    #     name = 'muestra-add'),

    url(r'^muestra/$',
        LabModule.app_views.Muestra.muestra_list,
        name = 'muestra-list'),

    url(r'^muestra/solicitar/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Muestra.muestra_request,
        name = 'muestra-request'),

    url(r'^muestra/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Muestra.muestra_detail,
        name = 'muestra-detail'),

    # url(r'^muestra/update/(?P<pk>[\w\-]+)/$',
    #     LabModule.app_views.Muestra.muestra_update,
    #     name = 'muestra-update'),

    # Servicios
    url(r'^maquina/events/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Solicitud.maquina_reservations,
        name = 's-maquina-reservations'),

    url(r'^solicitudes/experimentos/$',
        LabModule.app_views.Experimento.cargar_experimentos,
        name = 's-experimentos-list'),

    url(r'^solicitudes/protocolos/$',
        LabModule.app_views.Protocolo.cargar_protocolos,
        name = 's-protocolos-list'),

    url(r'^solicitudes/pasos/$',
        LabModule.app_views.Paso.cargar_pasos,
        name = 's-pasos-list'),

    # Solicitudes Muestras
    url(r'^solicitudes/muestras/$',
        LabModule.app_views.Solicitud.solicitud_muestra_list,
        name = 'solicitud-muestra-list'),

    url(r'^solicitudes/muestras/aprobar/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Solicitud.solicitud_muestra_aprobar,
        name = 'solicitud-muestra-aprobar'),

    url(r'^solicitudes/muestras/negar/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Solicitud.solicitud_muestra_negar,
        name = 'solicitud-muestra-negar'),

    url(r'^solicitudes/muestras/(?P<pk>[\w\-]+)/$',
        LabModule.app_views.Solicitud.solicitud_muestra_detail,
        name = 'solicitud-muestra-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
