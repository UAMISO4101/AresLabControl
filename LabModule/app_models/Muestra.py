# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

permissions_sample = (
    ('can_addSample', 'muestra||agregar'),
    ('can_editSample', 'muestra||editar'),
    ('can_listSample', 'muestra||listar'),
    ('can_viewSample', 'muestra||ver'),
    ('can_requestSample', 'muestra||solicitar'),
)


class Muestra(models.Model):
    """Representación de Muestra
         Se encarga de:
             * Definir las caracteristicas de un muestra
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre de la muestra
             :descripción (String): descripción de la muestra
             :valor (Numeric): Valor por unidad
             :activa (Boolean): Estado de disponibilidad de la muestra
             :controlado (Boolean): Estado de restriccion de la muestra
             :imagen (Image): Imagen de la muestra
             :unidadBase (String): Unidad de medida de la muestra
        Permisos:
            :can_addSample: Permite agregar muestra
            :can_editSample: Permite modificar muestra
            :can_viewSample: Permite ver muestra
      """

    class Meta:
        verbose_name = _('Muestra')
        verbose_name_plural = _('Muestras')
        permissions = permissions_sample

    nombre = models.CharField(
            max_length = 1000,
            blank = False,
            null = True,
            verbose_name = _("Nombre de la Muestra")
    )
    descripcion = models.TextField(
            max_length = 1000,
            blank = False,
            null = True,
            verbose_name = _("Descripción de la Muestra")
    )

    valor = models.DecimalField(
            max_digits = 5,
            decimal_places = 2,
            null = True,
            verbose_name = _("Valor")
    )
    activa = models.BooleanField(
            default = True,
            verbose_name = _("Activa")
    )
    controlado = models.BooleanField(
            blank = False,
            default = False,
            verbose_name = _("Muestra Controlada")
    )

    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )
    unidadBase = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Unidad de Medida")
    )

    def __unicode__(self):
        return 'Muestra: ' + self.nombre

    def calc_disp(self):
        from LabModule.app_models.Bandeja import Bandeja

        bandejas = Bandeja.objects.filter(muestra = self)
        for bandeja in bandejas:
            if not bandeja.libre:
                return 'Si'
        return 'No'
