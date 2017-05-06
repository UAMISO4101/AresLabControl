# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import inlineformset_factory

from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.Mueble import Mueble


class NMaquinaForm(ModelForm):
    class Meta:
        model = Maquina
        exclude = ['mueble']


MaquinaForm = inlineformset_factory(Mueble, Maquina, form = NMaquinaForm, can_delete = False)
