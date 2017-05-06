# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import inlineformset_factory

from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.Mueble import Mueble


class NAlmacenamientoForm(ModelForm):
    class Meta:
        model = Almacenamiento
        exclude = ['mueble']


AlmacenamientoForm = inlineformset_factory(Mueble, Almacenamiento, form = NAlmacenamientoForm, can_delete = False)
