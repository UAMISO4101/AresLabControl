# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.Solicitud import Solicitud


class SolicitudMaquina(models.Model):
    class Meta:
        verbose_name = _('Solicitud de Máquina')
        verbose_name_plural = _('Solicitudes de Máquina')

    solicitud = models.OneToOneField(Solicitud)
    maquina = models.ForeignKey(
            Maquina,
            blank = False,
            null = True,
            verbose_name = _("Selección de Máquina")
    )

    def __unicode__(self):
        return self.maquina.__unicode__() + " " + self.solicitud.__unicode__()

    def as_json(self, id_user):
        return dict(id_maquina = self.maquina.idSistema, id = self.solicitud.id,
                    encargado = self.solicitud.solicitante.nombre_completo(),
                    start = self.solicitud.fechaInicial.isoformat().replace('+00:00', '-05:00'),
                    end = self.solicitud.fechaFinal.isoformat().replace('+00:00', '-05:00'),
                    editable = False if id_user == self.solicitud.solicitante.user.id else False,
                    overlap = False, paso = self.solicitud.paso.nombre,
                    className = 'aprobada' if id_user == self.solicitud.solicitante.user.id
                                              and self.solicitud.estado == 'aprobada' else 'ocupada' if not id_user == self.solicitud.solicitante.user.id  else 'pendiente'
                    )
