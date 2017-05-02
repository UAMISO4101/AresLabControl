# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.Laboratorio import Laboratorio


class AlmacenamientoEnLab(models.Model):
    """Relación entre :class:`Almacenamiento` y :class:`Laboratorio`
        Se encarga de:
            * Definir la posición del lugar Almacenamiento en donde esta guardada
            * Permite guardar en la base de datos esta relación

        Atributos:
            :idLaboratorio (String): Id del laboratorio.
            :idLugar (String): Id del lugar Almacenamiento
            :posX (Integer): Posición x en la que el lugar Almacenamiento esta guardado.
            :posY (Integer): Posición y en la que el lugar Almacenamiento esta guardado.
     """

    class Meta:
        verbose_name = "Lugar de almacenamiento en Laboratorio"
        verbose_name_plural = 'Lugares de almacenamiento en Laboratorio'
        app_label = 'LabModule'

    idLaboratorio = models.ForeignKey(
            Laboratorio,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Laboratorio")
    )
    idLugar = models.OneToOneField(
            Almacenamiento,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = _("Lugar Almacenamiento"),
            primary_key = True
    )
    posX = models.PositiveIntegerField(
            verbose_name = _("Posición X")
    )
    posY = models.PositiveIntegerField(
            verbose_name = _("Posición Y")
    )

    def __unicode__(self):
        return self.idLaboratorio.id + ":" + str(self.posX) + "," + str(self.posY)
