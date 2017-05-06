# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Laboratorio import Laboratorio
from LabModule.app_models.Mueble import Mueble


class MuebleEnLab(models.Model):

    class Meta:
        verbose_name = _("Mueble en Laboratorio")
        verbose_name_plural = _('Muebles en Laboratorio')
        app_label = 'LabModule'
        unique_together = ('idLaboratorio', 'posX', 'posY')

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
    def es_ubicacion_rango(cls, id_laboratorio, new_posX, new_posY):
        tamano_maximo = Laboratorio.objects.get(idLaboratorio__exact = id_laboratorio).get_tamano_maximo()
        filas = tamano_maximo[0] < new_posX
        columnas = tamano_maximo[1] < new_posY
        return filas & columnas

    @classmethod
    def es_ubicacion_libre(cls, new_posX, new_posY):
        return not MuebleEnLab.objects.filter(posX__exact = new_posX).filter(posY__exact = new_posY).exists()
