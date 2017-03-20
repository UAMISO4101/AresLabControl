from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.home, name='login'),
    url(r'^logout/$', views.home, name='logout'),
    # Lugar de almacenamiento
    url(r'^agregarLugar/$', views.agregar_lugar, name='agregarLugar'),
    url(r'^listaLugares/$', views.listar_lugares, name='listaLugares'),

    url(r'^maquina/add/$', views.maquina_create, name='maquina-add'),
    url(r'^maquina/(?P<pk>[\w\-]+)/$',views.maquina_update, name='maquina-update'),
    url(r'^solicitarMuestra/$', views.make_sample_request, name='solicitarMuestra'),
    url(r'^solicitarMuestra/experiments/$', views.get_experiments, name='experimentos'),
    url(r'^solicitarMuestra/protocols/$', views.get_protocols, name='protocols'),
    url(r'^solicitarMuestra/steps/$', views.get_steps, name='steps'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)