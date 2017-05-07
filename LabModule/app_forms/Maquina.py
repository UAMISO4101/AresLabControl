# -*- coding: utf-8 -*-
from django.forms import ModelForm

from LabModule.app_models.Maquina import Maquina


class MaquinaForm(ModelForm):
    class Meta:
        model = Maquina
        exclude = ['mueble']
