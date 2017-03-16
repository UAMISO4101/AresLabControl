# coding=utf-8
from django import forms
from django.forms import ModelForm
from registration.forms import RegistrationForm

from .models import IdType as IdentificationTypes, LugarAlmacenamiento
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
    class Meta:
        model = LugarAlmacenamiento
        fields = ['nombre', 'descripcion', 'capacidad', 'temperatura', 'posX', 'posY', 'imagen', 'peso', 'tamano']
