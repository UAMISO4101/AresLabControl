# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from .models import Bandeja
from .models import LugarAlmacenamiento
from .models import LugarAlmacenamientoEnLab
from .models import Projecto
from .models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        exclude = ('user',)
    contrasena = forms.CharField(
        label="Escriba su contraseña",
        widget=forms.PasswordInput,
        strip=False,)
    password2 = forms.CharField(
        label="Confirme su contraseña",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Repita la contraseña para verificar que sean iguales.",
    )

    error_messages = {
        'password_mismatch': "Las contraseñas deben coincidir!",
    }

    def clean_password2(self):
        # Check that the two password entries match
        contrasena = self.cleaned_data.get("contrasena")
        password2 = self.cleaned_data.get("password2")
        if contrasena and password2 and contrasena != password2:
            raise forms.ValidationError("Las contraseñas no coinciden!")
        return contrasena

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
        model = LugarAlmacenamiento
        fields = ['nombre', 'descripcion', 'capacidad', 'temperatura', 'imagen', 'peso', 'tamano']


class PosicionesLugarAlmacenamientoForm(ModelForm):
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
        model = LugarAlmacenamientoEnLab
        fields = ['posX', 'posY', 'idLaboratorio']
        exclude = ('idLugar',)


class MuestraSolicitudForm(forms.Form):
    def __init__(self, muestra=None, id_asistente=None, *args, **kwargs):
        super(MuestraSolicitudForm, self).__init__(*args, **kwargs)
        if muestra != None and id_asistente != None:
            self.fields['id'] = forms.CharField(label="ID")
            self.fields['id'].initial = muestra.id
            self.fields['nombre'] = forms.CharField(label="NOMBRE")
            self.fields['nombre'].initial = muestra.nombre
            self.fields['descripcion'] = forms.CharField(label="DESCRIPCION")
            self.fields['descripcion'].initial = muestra.descripcion
            self.fields['unidad'] = forms.CharField(label="UNIDAD")
            self.fields['unidad'].initial = muestra.unidad
            self.fields['controlado'] = forms.CharField(label="CONTROLADA")
            self.fields['controlado'].initial = self.calc_controled(muestra.controlado)
            self.fields['disponible'] = forms.CharField(label="DISPONIBLE")
            self.fields['disponible'].initial = self.calc_disp(muestra)
            self.fields['imagen'] = forms.ImageField(label="IMAGEN")
            self.fields['imagen'].initial = muestra.imagen
            self.fields['cantidadActual'] = forms.CharField(label="CANTIDAD ACTUAL")
            self.fields['cantidadActual'].initial = muestra.cantidadActual
            self.fields['projectos'] = forms.MultipleChoiceField(
                required=True,
                widget=forms.CheckboxSelectMultiple,
                label="PROYECTO",
                choices=Projecto.objects.filter(
                    asistentes=id_asistente,
                    activo=True)
            )

    cantidad = forms.CharField(label="CANTIDAD")
    fechaInicial = forms.DateField(widget=forms.SelectDateWidget(), label="FECHA")

    def calc_controled(self, controlado):
        if controlado == True:
            return 'Si'
        else:
            return 'No'

    def calc_disp(self, nueva_muestra):
        bandejas = Bandeja.objects.filter(muestra=nueva_muestra)
        for bandeja in bandejas:
            if bandeja.libre == False:
                return 'Si'
        return 'No'
