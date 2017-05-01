# -*- coding: utf-8 -*-
from django.forms import ModelForm

from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.AlmacenamientoEnLab import AlmacenamientoEnLab


class LugarAlmacenamientoForm(ModelForm):
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
        fields = ['id', 'nombre', 'descripcion', 'capacidad', 'temperatura', 'imagen']
        # id=forms.CharField(error_messages={'Este campo es obigatorio,'})


class PosicionesAlmacenamientoForm(ModelForm):
    """Formulario  para crear y modificar la ubicación de un lugar almacenamiento.
        Se encarga de:
            * Tener una instancia del modelo del lugar almacenamiento en laboratorio.
            * Definir las posición x, la posición y y el laboratorio en el cual se va aguardar el lugar almacenamiento.
            * Agregar un lugar almacenamiento a la base de datos, agregar la relación entre el lugar almacenamiento y el laboratorio en el que está.
            * Modificar la ubicación de un lugar almacenamiento ya existente.
     :param ModelForm: Instancia de Django.forms.
     :type ModelForm: ModelForm.
    """

    class Meta:
        model = AlmacenamientoEnLab
        fields = ['posX', 'posY', 'idLaboratorio']
        exclude = ('idLugar',)
