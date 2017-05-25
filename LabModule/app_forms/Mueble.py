# -*- coding: utf-8 -*-
from django.forms import ModelForm

from LabModule.app_models.Mueble import Mueble
from LabModule.app_models.MuebleEnLab import MuebleEnLab


class MuebleForm(ModelForm):
    class Meta:
        model = Mueble
        fields = ['nombre', 'descripcion', 'estado', 'imagen']
        exclude = ('tipo',)


class PosicionesMuebleForm(ModelForm):
    class Meta:
        model = MuebleEnLab
        fields = ['idLaboratorio', 'posX', 'posY']
        exclude = ('idMueble',)

    def es_ubicacion_libre(self):
        if MuebleEnLab.es_ubicacion_libre(self.cleaned_data['idLaboratorio'],
                                          self.cleaned_data['posX'],
                                          self.cleaned_data['posY']):
            return True
        else:
            self.add_error('posX', "La fila ya esta ocupada")
            self.add_error('posY', "La columna ya esta ocupada")
        return False

    def es_el_mismo_mueble(self, mueble_id, idLaboratorio, posX, posY):
        try:
            old_mueble = MuebleEnLab.objects.get(idLaboratorio = idLaboratorio,
                                                 posX = posX,
                                                 posY = posY)
        except  MuebleEnLab.DoesNotExist:
            old_mueble = None
        if old_mueble == None:
            return True
        else:
            return mueble_id == old_mueble.idMueble.id

    def es_ubicacion_rango(self, posX, posY):
        lab = self.cleaned_data['idLaboratorio']
        masX = lab.numX >= posX
        masY = lab.numY >= posY
        posible = masX and masY
        if not posible:
            if not masX:
                self.add_error("posX", "La fila sobrepasa el valor máximo de " + str(lab.numX))
            if not masY:
                self.add_error("posY", "La columna sobrepasa el valor máximo de " + str(lab.numY))
            return False
        return True
