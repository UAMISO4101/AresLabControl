# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Laboratorio import Laboratorio
from LabModule.app_models.Mueble import Mueble


class MuebleEnLab(models.Model):

    class Meta:
        verbose_name = _("Mueble en Laboratorio")
        verbose_name_plural = _('Muebles en Laboratorio')

    idLaboratorio = models.ForeignKey(
            Laboratorio,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = "Laboratorio"
    )
    idMueble = models.OneToOneField(
            Mueble,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = "Mueble",
            primary_key = True,
            unique = True,
            error_messages = {'unique': "Ya existe un mueble con este ID"}
    )
    posX = models.PositiveIntegerField(
            verbose_name = "Columna",
            null = False,
            default = 0
    )
    posY = models.PositiveIntegerField(
            verbose_name = "Fila",
            null = False,
            default = 0
    )

    def __unicode__(self):
        return self.idLaboratorio.__unicode__() + ":" + str(self.posX) + "," + str(self.posY)


    @classmethod
    def es_ubicacion_libre(cls,id_lab, new_posX, new_posY):
        return not MuebleEnLab.objects.filter(idLaboratorio=id_lab,posX = new_posX,posY = new_posY).exists()
    @classmethod
    def get_laboratorio(cls,mueble):
        return  MuebleEnLab.objects.get(idMueble=mueble).idLaboratorio