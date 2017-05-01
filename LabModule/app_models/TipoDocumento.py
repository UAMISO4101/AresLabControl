# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _


class TipoDocumento(models.Model):
    """Representación del Tipos de Documento
        Se encarga de:
            * Definir los tipos de documentos a manejar en el sistema

        Atributos:
            :nombre_corto (String): Nnemotécnico Tipo Documento. Máxima longitud 5 caractéres.
            :descripcion (String): Descripción Tipo Documento. Máxima longitud 100 caractéres.
    """

    class Meta:
        verbose_name = _('Tipo Identificación')
        verbose_name_plural = _('Tipos de Indentificación')

    nombre_corto = models.CharField(
            max_length = 5,
            default = '',
            verbose_name = _('Abreviación Tipo Identificación')
    )
    descripcion = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _('Descripción Tipo Identificación')
    )

    def __unicode__(self):
        return self.nombre_corto
