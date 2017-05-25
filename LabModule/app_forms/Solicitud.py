# -*- coding: utf-8 -*-
import datetime

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

    def verificarDisponibilidad(self, start, end, fechaIni, fechaFin):
        d_end = datetime.datetime.strptime(end, "%Y-%m-%d")
        d_start = datetime.datetime.strptime(start, "%Y-%m-%d")
        d_fechaIni = datetime.datetime.strptime(fechaIni[:-6], "%Y-%m-%d")
        d_fechaFin = datetime.datetime.strptime(fechaFin[:-6], "%Y-%m-%d")
        if d_start <= d_fechaIni <= d_end and d_start <= d_fechaFin <= d_end:
            return True
        return False
