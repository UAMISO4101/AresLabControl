# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

permissions_protocol = (
    ('can_addProtocol', 'protocolo||agregar'),
    ('can_editProtocol', 'protocolo||editar'),
    ('can_listProtocol', 'protocolo||listar'),
    ('can_viewProtocol', 'protocolo||ver'),
)


class Protocolo(models.Model):
    """Representación de Protocolos
         Se encarga de:
             * Definir las caracteristicas de un protocolo
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre del protocolo.
             :descripción (String): descripción del protocolo
             :objetivo (String): Objetivo del protocolo
        Permisos:
            :can_addProtocol: Permite agregar protocolo
            :can_editProtocol: Permite modificar protocolo
            :can_viewProtocol: Permite ver protocolo
      """

    class Meta:
        verbose_name = _('Protocolo')
        verbose_name_plural = _('Protocolos')
        app_label = 'LabModule'
        permissions = permissions_protocol

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Nombre Protocolo")
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción del Protocolo")
    )
    objetivo = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Objetivo del Protocolo")
    )

    def __unicode__(self):
        return self.nombre
