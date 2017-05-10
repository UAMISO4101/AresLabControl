# -*- coding: utf-8 -*-
from django.forms import ModelForm

from LabModule.app_models.Almacenamiento import Almacenamiento


class AlmacenamientoForm(ModelForm):
    """Formulario  para crear y modificar el lugar almacenamiento.
           Se encarga de:
               * Tener una instancia del modelo del lugar almacenamiento en laboraotrio.
               * Agregar un lugar almacenamiento a la base de datos.
               * Modificar un lugar almacenamiento ya existente.
        :param ModelForm: Instancia de Django.forms.
        :type ModelForm: ModelForm.
       """

    class Meta:
        model = Almacenamiento
        exclude = ['mueble']
