# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms import ModelForm

from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMaquina import SolicitudMaquina


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fechaInicial', 'fechaFinal', 'descripcion', 'estado', 'solicitante', 'fechaActual', 'paso']
        widgets = {
            'fechaInicial': forms.DateInput(attrs = {'class': 'form-control date '}, format = ("%Y-%m-%d %H:%m")),
            'fechaFinal'  : forms.DateInput(attrs = {'class': 'form-control date '}, format = ("%Y-%m-%d %H:%m")),
        }

    def verificar_fecha(self, maquina_id, fechaIni, fechaFin):

        solicitudes = Solicitud.objects.filter(
                Q(fechaInicial = fechaIni, fechaFinal = fechaFin) |
                Q(fechaInicial__lt = fechaIni, fechaFinal__gt = fechaIni) |
                Q(fechaInicial__lte = fechaFin, fechaFinal__gte = fechaFin)).exclude(estado = 'rechazada')
        for sol in solicitudes:
            otras_maquinas = SolicitudMaquina.objects.filter(solicitud = sol.pk, maquina = maquina_id).count()
            if otras_maquinas > 0:
                return False
        return True
