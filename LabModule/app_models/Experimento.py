# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _

from LabModule.app_models.Protocolo import Protocolo
from LabModule.app_models.Proyecto import Proyecto

permissions_experiment = (
    ('can_addExperiment', 'experimento||agregar'),
    ('can_editExperiment', 'experimento||editar'),
    ('can_listExperiment', 'experimento||listar'),
    ('can_viewExperiment', 'experimento||ver'),
)


class Experimento(models.Model):
    """Representación de un experimento.
        Se encarga de:
            * Definir las caracteristicas de un experimento
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos esta entidad

        Atributos:
            :nombre (String): Nombre expermento
            :descripción (String): descripción del experimento.
            :objetivo (String): Objetivo del experimento
            :projecto (Decimal): Seleccion de Proyecto
            :protocolos (Object): Lista de protocolos
        Permisos:
            :can_addExperiment: Permite agregar experimento
            :can_editExperiment: Permite modificar experimento
            :can_viewExperiment: Permite ver experimento
    """

    class Meta:
        verbose_name = _('Experimento')
        verbose_name_plural = _('Experimentos')
        permissions = permissions_experiment

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Nombre Expermento")
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción del Experimento")
    )
    objetivo = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Objetivo del Experimento")
    )
    projecto = models.ForeignKey(
            Proyecto,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Proyecto"),
            related_name = "proyecto"
    )
    protocolos = models.ManyToManyField(
            Protocolo,
            related_name = "experimento"
    )

    def __unicode__(self):
        return self.nombre
