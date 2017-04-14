# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms import ModelForm

from .models import LugarAlmacenamiento, Muestra
from .models import LugarAlmacenamientoEnLab
from .models import Solicitud, MuestraSolicitud, MaquinaSolicitud
from .models import Usuario


class RegistroUsuarioForm(forms.ModelForm):
    """Formulario  para crear usuarios.
           Se encarga de:
               * Tener una instancia del modelo del usuario.
               * Agregar un usuario a la base de datos.

        :param ModelForm: Instancia de Django.forms.
        :type ModelForm: ModelForm.
       """

    class Meta:
        model = Usuario
        exclude = ('user',)

    contrasena = forms.CharField(
        label="Escriba su contraseña",
        widget=forms.PasswordInput,
        strip=False, )
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


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fechaInicial', 'fechaFinal', 'descripcion', 'estado', 'solicitante', 'fechaActual', 'paso']
        widgets = {
            'fechaInicial': forms.DateInput(attrs={'class': 'datepicker'}),
            'fechaFinal': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def verificar_fecha(self, maquina_id, fechaIni, fechaFin):

        solicitudes = Solicitud.objects.filter(
            Q(fechaInicial=fechaIni, fechaFinal=fechaFin) | Q(fechaInicial__lte=fechaIni, fechaFinal__gte=fechaIni) | Q(
                fechaInicial__lte=fechaFin, fechaFinal__gte=fechaFin)).exclude(estado='rechazada')
        for sol in solicitudes:
            otras_maquinas = MaquinaSolicitud.objects.filter(solicitud=sol.pk, maquina=maquina_id).count()
            if otras_maquinas > 0:
                return False
        return True


class MuestraSolicitudForm(ModelForm):
    class Meta:
        model = MuestraSolicitud
        fields = ['cantidad', 'solicitud', 'muestra', 'tipo']


class MuestraForm(ModelForm):
    """Formulario  para crear y modificar muestras.
           Se encarga de:
               * Tener una instancia del modelo muestra.
               * Agregar una muestra a la base de datos.
               * Modificar una muestra ya existente.
        :param ModelForm: Instancia de Django.forms.
        :type ModelForm: ModelForm.
       """

    class Meta:
        model = Muestra
        fields = ['nombre', 'descripcion', 'imagen']
