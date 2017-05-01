# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.Solicitud import Solicitud


class SolicitudMuestra(models.Model):
    """Relación entre :class:`Muestra` y :class:`Solicitud` Detalle de solicitud
        Se encarga de:
            * Definir la relacion entre solicitud y muestras solicitadas
            * Permite guardar en la base de datos el detalle de una solicitud

        Atributos:
            :solicitud (Decimal): Id solicitud.
            :muestra (Decimal): Selección de Muestra
            :cantidad (Integer): Cantidad de muestra.
            :tipo (String):Tipo solicitud.
        Permisos:
            :can_solMuestra: Permite solicitar muestra
         """

    class Meta:
        verbose_name = _('Solicitud de Muestra')
        verbose_name_plural = _('Solicitudes de Muestra')

    solicitud = models.OneToOneField(Solicitud)
    muestra = models.ForeignKey(
            Muestra,
            blank = False,
            null = True,
            verbose_name = _("Selección de Muestra")
    )
    cantidad = models.IntegerField(
            blank = False,
            null = True,
            default = 1,
            verbose_name = _("Cantidad de Muestra")
    )
    tipo = models.CharField(
            max_length = 30,
            blank = False,
            null = True,
            verbose_name = _("Tipo Solicitud")
    )
