# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    nombre = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _('Nombre')
    )
    descripcion = models.TextField(
            max_length = 1000,
            default = '',
            verbose_name = _("Descripción")
    )

    capacidad = models.PositiveIntegerField(
            verbose_name = _("Capacidad")
    )
    temperatura = models.DecimalField(
            max_digits = 5,
            decimal_places = 2,
            verbose_name = _("Temperatura")
    )
    estado = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _('Estado'),
            null = True
    )
    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )

    id = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Identificación"),
            null = False,
            primary_key = True
    )

    def __unicode__(self):
        return str(self.pk) + ":" + self.nombre
