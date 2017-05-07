# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory

from LabModule.app_models.Almacenamiento import Almacenamiento


class AlmacenamientoForm(ModelForm):
	class Meta:
		model = Almacenamiento
		exclude = ['mueble']

