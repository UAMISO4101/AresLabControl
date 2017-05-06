# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

permissions_lab = (
    ('can_addLab', 'laboratorio||agregar'),
    ('can_editLab', 'laboratorio||editar'),
    ('can_listLab', 'laboratorio||listar'),
    ('can_viewLab', 'laboratorio||ver'),
)


class Laboratorio(models.Model):
    """Representación del laboratorio
        Se encarga de:
            * Definir un laboratorio y los campos significativos
            * Permite guardar en la base de datos el laboratorio.

        Atributos:
            :nombre (String): Nombre del laboratorio. Máxima longitud de 100 caractéres. No puede ser nulo
            :idLaboratorio (String): Id del laboratorio. Identificación del laboratorio, campo único, 
                          máxima longitud de 100 caractéres.
            :numX (Integer): Cantidad de columnas que tiene el laboratorio para almacenar máquinas. Por defecto 10.
            :numY (Integer): Cantidad de filas que tiene el laboratorio para alamacenar máquinas. Por defecto 10.

        Permisos:
            :can_addLab: Permite agregar Laboratorios
            :can_edditLab: Permite modificar Laboratorios
    """

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        app_label = 'LabModule'
        permissions = permissions_lab

    idLaboratorio = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Identificación"),
            null = False,
            primary_key = True
    )
    nombre = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Nombre"),
            null = False
    )

    numX = models.PositiveIntegerField(
            verbose_name = _("Cantidad de Filas"),
            null = False,
            default = 10
    )
    numY = models.PositiveIntegerField(
            verbose_name = _("Cantidad de Columnas"),
            null = False,
            default = 10
    )

    def __unicode__(self):
        return self.idLaboratorio.capitalize() + " " + self.nombre.capitalize()
