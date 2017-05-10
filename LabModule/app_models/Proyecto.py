# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Usuario import Usuario

permissions_project = (
    ('can_addProject', 'proyecto||agregar'),
    ('can_editProject', 'proyecto||editar'),
    ('can_listProject', 'proyecto||listar'),
    ('can_viewProject', 'proyecto||ver'),
)


class Proyecto(models.Model):
    """Representación de un proyecto.
        Se encarga de:
            * Definir las caracteristicas de un proyecto
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos esta entidad

        Atributos:
            :nombre (String): Nombre proyecto
            :descripción (String): descripción del proyecto.
            :objetivo (String): Objetivo del proyecto
            :lider (Decimal): Seleccion lider
            :asistentes (Object): Lista de asistentes
            :activo (Boolean): Estado de actividad del proyecto
        Permisos:
            :can_addProject: Permite agregar Proyecto
            :can_editProject: Permite modificar Proyecto
            :can_viewProject: Permite ver Proyecto
    """

    class Meta:
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')
        app_label = 'LabModule'
        permissions = permissions_project

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Nombre del Proyecto")
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción del Proyecto")
    )
    objetivo = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Objetivo del Proyecto")
    )
    lider = models.ForeignKey(
            Usuario,
            blank = False,
            null = True,
            verbose_name = _("Líder"),
            related_name = 'li_%(app_label)s_%(class)s_related'
    )
    asistentes = models.ManyToManyField(
            Usuario,
            verbose_name = _("Asistentes"),
            related_name = 'as_%(app_label)s_%(class)s_related'
    )
    activo = models.BooleanField(
            blank = False,
            null = False,
            default = True,
            verbose_name = _('Estado de Actividad del Proyecto')
    )

    def __unicode__(self):
        return self.nombre
