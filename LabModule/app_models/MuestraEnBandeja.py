# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.Muestra import Muestra


class MuestraEnBandeja(models.Model):
    class Meta:
        verbose_name = "Muestra en Bandeja"
        verbose_name_plural = "Muestras en Bandeja"
        app_label = "LabModule"
        unique_together = ('idBandeja', 'posX', 'posY')

    idBandeja = models.ForeignKey(
            Bandeja,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Bandeja"),
            related_name = '%(app_label)s_%(class)s_related'
    )
    idMuestra = models.ForeignKey(
            Muestra,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = _("Muestra"),
            related_name = '%(app_label)s_%(class)s_related'
    )
    posX = models.PositiveIntegerField(
            verbose_name = _("Fila"),
            default = 1,
    )
    posY = models.PositiveIntegerField(
            verbose_name = _("Columna"),
            default = 1,
    )

    def __unicode__(self):
        return str(self.posX) + ":" + str(self.posY)
