# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

permissions_machine = (
    ('can_addMachine', 'maquina||agregar'),
    ('can_editMachine', 'maquina||editar'),
    ('can_listMachine', 'maquina||listar'),
    ('can_viewMachine', 'maquina||ver'),
    ('can_requestMachine', 'maquina||solicitar'),
)


class Maquina(models.Model):
    """Representación de una máquina.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la máquina

        Atributos:
            :nombre (String): Nombre de la máquina, máxima longitud 100 caractéres, no puede ser nulo.
            :descripción (String): Descripción de la máquina,  máxima longitud 1000 caractéres, no puede ser nulo.
            :imagen (ImafeField): Imágen de la máquina,  default='images/image-not-found.jpg'.
            :idSistema (String): Identificación del laboratorio, máxima longitud de 20 caractéres.
            :con_reserva (boolean): Dice si es necesario aprobar la máquina para ser reservada. Por defecto verdadero
            :activa (boolean): Dice si la máquina se puede solicitar. Por defecto verdadero

        Permisos:
            :can_addMachine: Permite agregar maquinas
            :can_edditMachine: Permite modificar maquinas
            :can_viewMachine: Permite modificar maquinas
            """

    class Meta:
        verbose_name = _("Máquina")
        verbose_name_plural = _('Máquinas')
        app_label = 'LabModule'
        permissions = permissions_machine

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
    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )
    idSistema = models.CharField(
            max_length = 20,
            default = '',
            verbose_name = _("Identificación"),
            null = False,
            primary_key = True
    )
    con_reserva = models.BooleanField(
            default = True,
            verbose_name = _("Reservable")
    )
    activa = models.BooleanField(
            default = True,
            verbose_name = _("Activa")
    )

    def __unicode__(self):
        return self.idSistema + " " + self.nombre

    def get_absolute_url(self):
        return reverse('author-detail', kwargs = {'pk': self.pk})
