from django.contrib import admin

from LabModule import models
from .models import UserRole, UserProfile, IdType,MaquinaProfile, LaboratorioProfile,MaquinaEnLab, Muestra, Projecto, \
    Experimento, Protocolo, Paso, Solicitud, MuestraSolicitud


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["__unicode__"]

    class Meta:
        model = UserRole


class IdTypeAdmin(admin.ModelAdmin):
    class Meta:
        model = IdType


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "userCode", "user", "userRole"]

    class Meta:
        model = UserProfile


# Register your models here.
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(IdType, IdTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
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
