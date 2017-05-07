# -*- coding: utf-8 -*-

from django.contrib import admin

from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.AlmacenamientoEnLab import AlmacenamientoEnLab
from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.Experimento import Experimento
from LabModule.app_models.Laboratorio import Laboratorio
from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.MaquinaEnLab import MaquinaEnLab
from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Protocolo import Protocolo
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMaquina import SolicitudMaquina
from LabModule.app_models.SolicitudMuestra import SolicitudMuestra
from LabModule.app_models.TipoDocumento import TipoDocumento
from LabModule.app_models.Usuario import Usuario
from LabModule.app_models.Mueble import Mueble
from LabModule.app_models.MuebleEnLab import MuebleEnLab


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "descripcion"]

    class Meta:
        model = TipoDocumento


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "correo_electronico", "codigo_usuario"]

    class Meta:
        model = Usuario


# Register your models here.
admin.site.register(Almacenamiento)
admin.site.register(AlmacenamientoEnLab)
admin.site.register(Bandeja)
admin.site.register(Experimento)
admin.site.register(Laboratorio)
admin.site.register(Maquina)
admin.site.register(MaquinaEnLab)
admin.site.register(Muestra)
admin.site.register(Paso)
admin.site.register(Protocolo)
admin.site.register(Proyecto)
admin.site.register(Solicitud)
admin.site.register(SolicitudMaquina)
admin.site.register(SolicitudMuestra)
admin.site.register(MuebleEnLab)
admin.site.register(Mueble)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
