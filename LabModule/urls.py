from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.home, name='login'),
    url(r'^logout/$', views.home, name='logout'),
    url(r'^register/$', views.home, name='register'),

    # Lugar de almacenamiento
    url(r'^agregarLugar/$', views.agregar_lugar, name='agregarLugar'),
    url(r'^maquina/add/$', views.maquina_create, name='maquina-add'),
    url(r'^maquina/(?P<pk>[0-9]+)/$',views.maquina_update, name='maquina-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)