# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from LabModule.app_models.Maquina import Maquina


class MaquinaForm(ModelForm):
    """Formulario  para crear y modificar una máquina.
          Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
          Historia de usuario: `ALF-20 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-20 />`_ :Yo como Jefe de Laboratorio quiero poder filtrar las máquinas existentes por nombre para visualizar sólo las que me interesan.
          Historia de usuario: `ALF-25 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-25 />`_ :Yo como Asistente de Laboratorio quiero poder filtrar las máquinas existentes por nombre para visualizar sólo las que me interesan.
              Se encarga de:
                * Tener una instancia del modelo de la máquina
                * Seleccionar cuales campos del modelo seran desplegados en el formulario. Nombre, descripción, si esta reservado,activa
                  y la id dada por el sistema.
                * Agregar una máquina a la base de datos, agregar la relación entre la máquina y el laboratorio en el que está.
                * Modificar los datos  de una máquina ya existente.
           :param ModelForm: Instancia de Django.forms.
           :type ModelForm: ModelForm.
    """
    fechaInicialDisp = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M"
                                                      ] )
    fechaFinalDisp = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M"])
    class Meta:
        model = Maquina
        exclude = ['mueble']

        #widgets = {
        #    'fechaInicialDisp': forms.DateInput(attrs={'class': 'form-control date '}),
        #    'fechaFinalDisp': forms.DateInput(attrs={'class': 'form-control date '})
        #}
