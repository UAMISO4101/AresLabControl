from django.conf.urls import url

from . import views

urlpatterns = [
    # Peticiones a vistas
    url(r'^$', views.home, name='home'),
]
