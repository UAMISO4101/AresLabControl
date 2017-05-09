# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.Protocolo import Protocolo

permissions_step = (
    ('can_addStep', 'paso||agregar'),
    ('can_editStep', 'paso||editar'),
    ('can_listStep', 'paso||listar'),
    ('can_viewStep', 'paso||ver'),
)


class Paso(models.Model):
    """Representación de Paso
         Se encarga de:
             * Definir las caracteristicas de un paso
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre del paso.
             :descripción (String): descripción del paso
             :protocolo (Relacion): Seleccion de Protocolo
        Permisos:
            :can_addStep: Permite agregar paso
            :can_editStep: Permite modificar paso
            :can_viewStep: Permite ver paso
      """

    class Meta:
        verbose_name = _('Paso')
        verbose_name_plural = _('Pasos')
        app_label = 'LabModule'
        permissions = permissions_step

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = "Nombre de Paso"
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = "Descripción del Paso"
    )
    protocolo = models.ForeignKey(
            Protocolo,
            blank = False,
            null = True,
            verbose_name = "Selección de Protocolo",
            related_name = '%(app_label)s_%(class)s_related'
    )
    muestras = models.ManyToManyField(
            Muestra,
            related_name = '%(app_label)s_%(class)s_related'
    )

    def __unicode__(self):
        return self.nombre
