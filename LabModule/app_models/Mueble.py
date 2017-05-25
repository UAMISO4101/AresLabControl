# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _


class Mueble(models.Model):
    class Meta:
        verbose_name = _("Mueble")
        verbose_name_plural = _('Muebles')
        app_label = 'LabModule'

    nombre = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Nombre"),
            null = False
    )

    descripcion = models.CharField(
            max_length = 1000,
            default = '',
            verbose_name = _("Descripción"),
            null = True
    )

    estado = models.BooleanField(
            default = True,
            verbose_name = _('Activa'),
            null = False
    )

    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )

    tipo = models.CharField(
            max_length = 1000,
            default = 'Desconocido',
            verbose_name = _("Descripción"),
            null = False
    )

    def __unicode__(self):
        return self.nombre

    def get_nombre(self):
        return self.nombre.capitalize()

    def get_descripcion(self):
        return self.descripcion.capitalize()

    def get_estado(self):
        return self.estado

    def get_imagen(self):
        return self.imagen
