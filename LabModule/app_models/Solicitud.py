# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Paso import Paso
from LabModule.app_models.Usuario import Usuario

permissions_request = (
    ('can_listRequest', 'solicitud||listar'),
    ('can_viewRequest', 'solicitud||ver'),
    ('can_manageRequest', 'solicitud||admin'),
)


class Solicitud(models.Model):
    """Representación de una bandeja del lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la solicitud

        Atributos:
            :tamano (String): Tamaño de la bandeja del lugar de almacenamiento.
            :cantidad (Integer): Cantidad de la bandeja del lugar de almacenamiento.
            :libre (Decimal): Indica si esta libre la bandeja del lugar de almacenamiento.
            :muestra (String): Relación con la entidad muestra.
            :lugarAlmacenamiento (Decimal): Relación con la entidad lugar de almacenamiento.
    """

    class Meta:
        verbose_name = _('Solicitud')
        verbose_name_plural = _('Solicitudes')
        app_label = 'LabModule'
        permissions = permissions_request

    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción de la Solicitud")
    )
    fechaInicial = models.DateTimeField(
            blank = False,
            null = True,
            verbose_name = _("Fecha Inicial"),
            default = timezone.now

    )
    fechaFinal = models.DateTimeField(
            blank = False,
            null = True,
            verbose_name = _("Fecha Final"),
            default = timezone.now
    )
    estado = models.CharField(
            max_length = 30,
            blank = False,
            null = True,
            verbose_name = _("Estado Solicitud")
    )
    solicitante = models.ForeignKey(
            Usuario,
            blank = False,
            null = True,
            verbose_name = _("Solicitante"),
            related_name = "solicitudesHechas"
    )
    aprobador = models.ForeignKey(
            Usuario,
            blank = False,
            null = True,
            verbose_name = _("Aprobador"),
            related_name = "solicitudesAprobadas"
    )
    fechaActual = models.DateField(
            blank = False,
            null = True,
            verbose_name = _("Fecha Actual"),
            default = timezone.now
    )
    paso = models.ForeignKey(
            Paso,
            blank = False,
            null = True,
            verbose_name = _("Selección de Paso")
    )

    def __unicode__(self):
        return self.solicitante.__unicode__() + " " + self.estado
