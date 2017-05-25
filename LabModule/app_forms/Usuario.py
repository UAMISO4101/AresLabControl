# -*- coding: utf-8 -*-
from django import forms

from LabModule.app_models.Usuario import Usuario


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
            label = "Escriba su contraseña",
            widget = forms.PasswordInput,
            strip = False, )
    password2 = forms.CharField(
            label = "Confirme su contraseña",
            widget = forms.PasswordInput,
            strip = False,
            help_text = "Repita la contraseña para verificar que sean iguales.",
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
