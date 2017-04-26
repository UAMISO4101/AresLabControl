# -*- coding: utf-8 -*-

from django.contrib import admin

from models import Bandeja
from models import Experimento
from models import LaboratorioProfile
from models import LugarAlmacenamiento
from models import LugarAlmacenamientoEnLab
from models import MaquinaEnLab
from models import MaquinaProfile
from models import MaquinaSolicitud
from models import Muestra
from models import MuestraSolicitud
from models import Paso
from models import Protocolo
from models import Proyecto
from models import Solicitud
from models import TipoDocumento
from models import Usuario


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "descripcion"]

    class Meta:
        model = TipoDocumento


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "correo_electronico", "codigo_usuario"]

    class Meta:
        model = Usuario


# Register your models here.
admin.site.register(Experimento)
admin.site.register(LaboratorioProfile)
admin.site.register(MaquinaEnLab)
admin.site.register(MaquinaProfile)
admin.site.register(Muestra)
admin.site.register(MuestraSolicitud)
admin.site.register(Paso)
admin.site.register(Proyecto)
admin.site.register(Protocolo)
admin.site.register(Solicitud)
admin.site.register(Bandeja)
admin.site.register(LugarAlmacenamientoEnLab)
admin.site.register(MaquinaSolicitud)
admin.site.register(LugarAlmacenamiento)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
