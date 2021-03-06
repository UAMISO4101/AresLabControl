# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Mueble import Mueble

permissions_storage = (
    ('can_addStorage', 'almacenamiento||agregar'),
    ('can_editStorage', 'almacenamiento||editar'),
    ('can_listStorage', 'almacenamiento||listar'),
    ('can_viewStorage', 'almacenamiento||ver'),
    ('can_requestStorage', 'almacenamiento||solicitar'),
)


class Almacenamiento(models.Model):
    """Representación de un lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos el lugar de almacenamiento

        Atributos:
            :nombre (String): Nombre del lugar de almacenamiento.
            :descripción (String): Descripción del lugar de almacenamiento
            :capacidad (Integer): Capacidad del lugar de almacenamiento.
            :temperatura (Decimal): Temperatura del lugar de almacenamiento.
            :estado (String): Estado del lugar de almacenamiento.
            :imagen (ImafeField): Imágen de lugar de almacenamiento,  default='images/image-not-found.jpg'.
        Permisos:
            :can_addStorage: Permite agregar Almacenamientos
            :can_editStorage: Permite modificar Almacenamientos
            :can_viewStorage: Permite ver Almacenamientos
    """

    class Meta:
        verbose_name = _('Lugar Almacenamiento')
        verbose_name_plural = _('Lugares de Almacenamiento')
        app_label = 'LabModule'
        permissions = permissions_storage

    idSistema = models.CharField(
            max_length = 20,
            default = '',
            verbose_name = _("Identificación"),
            null = False,
            primary_key = True
    )

    mueble = models.OneToOneField(
            Mueble,
            null=True,
            on_delete = models.CASCADE,
            related_name = '%(app_label)s_%(class)s_related'
    )

    temperatura = models.DecimalField(
            max_digits = 5,
            decimal_places = 2,
            verbose_name = _("Temperatura"),
            default = 25,
    )

    numX = models.PositiveIntegerField(
            verbose_name = _("Máximo Filas"),
            default = 1,
    )
    numY = models.PositiveIntegerField(
            verbose_name = _("Máximo Columnas"),
            default = 1,
    )
    numZ = models.PositiveIntegerField(
            verbose_name = _("Máximo Bandejas"),
            default = 1,
    )

    def __unicode__(self):
        return self.idSistema+ self.mueble.__unicode__()

    def get_id_sistema(self):
        return self.idSistema

    def get_nombre(self):
        return self.mueble.get_nombre()

    def get_descripcion(self):
        return self.mueble.get_descripcion()

    def get_estado(self):
        return self.mueble.get_estado()

    def get_max_capacidad(self):
        return self.numZ * self.numY * self.numX

    def get_absolute_url(self):
        return reverse('author-detail', kwargs = {'pk': self.pk})
