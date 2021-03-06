# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Almacenamiento import Almacenamiento

permissions_tray = (
    ('can_addTray', 'bandeja||agregar'),
    ('can_editTray', 'bandeja||editar'),
    ('can_listTray', 'bandeja||listar'),
    ('can_viewTray', 'bandeja||ver'),
)


class Bandeja(models.Model):
    """Representación de una bandeja del lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la bandeja del lugar de almacenamiento

        Atributos:

            :libre (Decimal): Indica si esta libre la bandeja del lugar de almacenamiento.
            :muestra (String): Relación con la entidad muestra.
            :lugarAlmacenamiento (Decimal): Relación con la entidad lugar de almacenamiento.
    """

    class Meta:
        verbose_name = _('Bandeja')
        verbose_name_plural = _('Bandejas')
        app_label = 'LabModule'
        permissions = permissions_tray
        unique_together = ('almacenamiento', 'posicion')

    almacenamiento = models.ForeignKey(
            Almacenamiento,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Selección de Lugar Almacenamiento"),
            related_name = '%(app_label)s_%(class)s_related'
    )

    posicion = models.PositiveIntegerField(
            verbose_name = _("Número de bandeja"),
            null = False,
            default = 1,
            blank = False
    )

    def __unicode__(self):
        return 'Bandeja: ' + self.almacenamiento.get_id_sistema() + " " + str(self.posicion)
    @classmethod
    def getBandejas(cls,idLugar):
        return Bandeja.objects.filter(almacenamiento=idLugar)