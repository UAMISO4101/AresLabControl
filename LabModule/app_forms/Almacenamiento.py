# -*- coding: utf-8 -*-
from django.forms import ModelForm

from LabModule.app_models.Almacenamiento import Almacenamiento


class AlmacenamientoForm(ModelForm):
    class Meta:
        model = Almacenamiento
        exclude = ['mueble']
