# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.Laboratorio import Laboratorio
from LabModule.app_models.Maquina import Maquina


class MaquinaEnLab(models.Model):
    """Relación entre :class:`Maquina` y :class:`Laboratorio`
        Se encarga de:
            * Definir la posición del laboratorio en que la máquina esta guardada
            * Permite guardar en la base de datos esta relación

        Atributos:
            :idLaboratorio (String): Id del laboratorio en el que la máquina esta guardada.
            :idMaquina (String): Id de la máquina que esta guaradada
            :posX (Integer): Posición x en la que la máquina esta guardada. No puede ser nulo, por defecto 0.
            :posY (Integer): Posición y en la que la máquina esta guardada. No puede sr nulo, por defecto 0.
    """

    class Meta:
        verbose_name = _("Máquina en Laboratorio")
        verbose_name_plural = _('Máquinas en Laboratorio')
        app_label = 'LabModule'


    idLaboratorio = models.ForeignKey(
            Laboratorio,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = "Laboratorio"
    )
    idMaquina = models.OneToOneField(
            Maquina,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = "Máquina",
            primary_key = True,
            unique = True,
            error_messages = {'unique': "Ya existe una máquina con este ID"}
    )
    posX = models.PositiveIntegerField(
            verbose_name = "Fila",
            null = False,
            default = 0
    )
    posY = models.PositiveIntegerField(
            verbose_name = "Columna",
            null = False,
            default = 0
    )

    def __unicode__(self):
        return self.idLaboratorio.__unicode__() + ":" + str(self.posX) + "," + str(self.posY)
