# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Cargo
from .models import Experimento
from .models import LaboratorioProfile
from .models import MaquinaEnLab
from .models import MaquinaProfile
from .models import Muestra
from .models import MuestraSolicitud
from .models import Paso
from .models import Projecto
from .models import Protocolo
from .models import Solicitud
from .models import TipoDocumento
from .models import Usuario


class CargoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__"]

    class Meta:
        model = Cargo


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "descripcion"]

    class Meta:
        model = TipoDocumento


<<<<<<< HEAD
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "userCode", "user"]
=======
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "correo_electronico", "codigo_usuario"]
>>>>>>> master

    class Meta:
        model = Usuario


# Register your models here.
admin.site.register(Cargo, CargoAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(MaquinaProfile)
admin.site.register(Muestra)
admin.site.register(Projecto)
admin.site.register(Experimento)
admin.site.register(Protocolo)
admin.site.register(Paso)
admin.site.register(Solicitud)
admin.site.register(MuestraSolicitud)
admin.site.register(LaboratorioProfile)
admin.site.register(MaquinaEnLab)
