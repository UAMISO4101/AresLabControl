# -*- coding: utf-8 -*-
from django import forms

# coding=utf-8
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.forms import ModelForm, widgets
from registration.forms import RegistrationForm

from .models import IdType as IdentificationTypes, LugarAlmacenamiento, Bandeja, Projecto, LugarAlmacenamientoEnLab, \
    MaquinaEnLab, LaboratorioProfile, Solicitud, MuestraSolicitud, MaquinaSolicitud
from .models import UserRole as UsrRole


class UserProfileForm(RegistrationForm):
    idTypName = IdentificationTypes.objects.all()
    usrroles = UsrRole.objects.all()

    username = forms.CharField(
        label="Nombre de Usuario",
        disabled=False
    )
    error_messages = {
        'password_mismatch': "Las contraseñas deben coincidir!",
    }
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirme su contraseña",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Repita la contraseña para verificar que sean iguales.",
    )
    userNatIdTypName = forms.ModelChoiceField(
        label="Tipo de Identificación",
        queryset=idTypName,
        empty_label="Seleccione una opción")

    userNatIdNum = forms.CharField(
        label="Número de Identificación"
    )

    userGivenName = forms.CharField(
        label="Nombres"
    )

    userLastName = forms.CharField(
        label="Apellidos"
    )

    userCode = forms.CharField(
        label="Código de Usuario",
        strip=True
    )
    userPhone = forms.CharField(
        label="Número de Teléfono"
    )
    userRoleName = forms.ModelChoiceField(
        label="Cargo",
        queryset=usrroles,
        empty_label="Seleccione una opción"
    )


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
        model=LugarAlmacenamientoEnLab
        fields = ['posX', 'posY', 'idLaboratorio']
        exclude = ('idLugar',)


class SolicitudForm(ModelForm):

    class Meta:
        model=Solicitud
        fields = ['fechaInicial', 'fechaFinal', 'descripcion', 'estado', 'solicitante', 'fechaActual', 'paso']
        widgets = {
            'fechaInicial': forms.DateInput(attrs={'class': 'datepicker'}),
            'fechaFinal': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def verificar_fecha(self,maquina_id, fechaIni, fechaFin):

        solicitudes = Solicitud.objects.filter(
            Q(fechaInicial=fechaIni, fechaFinal=fechaFin) | Q(fechaInicial__lte=fechaIni,fechaFinal__gte=fechaIni) | Q(
                fechaInicial__lte=fechaFin, fechaFinal__gte=fechaFin)).exclude(estado='rechazada')
        for sol in solicitudes:
            otras_maquinas = MaquinaSolicitud.objects.filter(solicitud=sol.pk, maquina=maquina_id).count()
            if otras_maquinas > 0:
                return False
        return True

class MuestraSolicitudForm(ModelForm):
    class Meta:
        model=MuestraSolicitud
        fields=['cantidad','solicitud','muestra','tipo']








