from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name = 'home'),
    # Lugar de almacenamiento
    url(r'^almacenamiento/add/$', views.lugar_add, name = 'lugar-add'),
    url(r'^almacenamiento/update/(?P<pk>[\w\-]+)/$', views.lugar_detail, name = 'lugar-update'),
    url(r'^almacenamiento/(?P<pk>[\w\-]+)/$', views.lugar_detail, name = 'lugar-detail'),
    url(r'^almacenamiento/$', views.lugar_list, name = 'lugar-list'),
    # Usuarios
    url(r'accounts/register/$', views.registrar_usuario, name = 'registration_register'),
    # Maquinas
    url(r'^maquina/add/$', views.maquina_add, name = 'maquina-add'),
    url(r'^maquina/$', views.maquina_list, name = 'maquina-list'),
    url(r'^maquina/solicitar/$', views.maquina_request, name = 'maquina-request'),
    # url(r'^maquina/solicitar/(?P<pk>[\w\-]+)/$', views.maquina_request, name = 'maquina-request'),
    url(r'^maquina/(?P<pk>[\w\-]+)/$', views.maquina_detail, name = 'maquina-detail'),
    url(r'^maquina/update/(?P<pk>[\w\-]+)/$', views.maquina_update, name = 'maquina-update'),
    # Muestras
    # url(r'^muestra/add/$', views.muestra_create, name = 'muestra-add'),
    url(r'^muestra/$', views.muestra_list, name = 'muestra-list'),
    url(r'^muestra/solicitar/$', views.muestra_request, name = 'muestra-request'),
    url(r'^muestra/(?P<pk>[\w\-]+)/$', views.muestra_detail, name = 'muestra-detail'),
    # url(r'^muestra/update/(?P<pk>[\w\-]+)/$', views.muestra_update, name = 'muestra-update'),
    # Servicios
    url(r'^solicitarMuestra/experimentos/$', views.cargar_experimentos, name = 's-experimentos-list'),
    url(r'^solicitarMuestra/protocolos/$', views.cargar_protocolos, name = 's-protocolos-list'),
    url(r'^solicitarMuestra/pasos/$', views.cargar_pasos, name = 's-pasos-list'),
    # Solicitudes
    url(r'^aprobarSolicitudMuestras/listar/$', views.listar_solicitud_muestra, name = 'solicitudes-muestra-list'),
    url(r'^aprobarSolicitudMuestras/aprobar/$', views.aprobar_solicitud_muestra, name = 'solicitud-muestra-aprobar'),
    # Schedule
    url(r'^maquina/events/(?P<pk>[\w\-]+)/$', views.maquina_reservations, name = 'maquina-reservations'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
