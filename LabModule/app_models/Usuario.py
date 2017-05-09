# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from LabModule.app_models.TipoDocumento import TipoDocumento

USERNAME_REGEX = '^[a-zA-Z0-9.-_]*$'
USERMAIL_REGEX = '^[a-zA-Z0-9.@-_]*$'
USERCODE_REGEX = '^[a-zA-Z0-9]*$'

permissions_user = (
    ('can_addUser', 'usuario||agregar'),
    ('can_editUser', 'usuario||editar'),
    ('can_listUser', 'usuario||listar'),
    ('can_viewUser', 'usuario||ver'),
)


class Usuario(models.Model):
    """Representación de Usuarios
        Se encarga de:
            * Definir los usuarios y sus atributos

        Atributos:
            :nombre_usuario (String): Nombre de usuario. Máxima longitud 255 caractéres, único.
            :correo_electronico (String): Correo electronico. Máxima longitud 255 caractéres, único.
            :codigo_usuario (String): Código de usuario. Máxima longitud 20 caractéres, único.
            :nombres (String): Nombres. Máxima longitud 50 caractéres.
            :apellidos (String): Apellidos. Máxima longitud 50 caractéres.
            :telefono (String): Teléfono. Máxima longitud 20 caractéres.
            :userNatIdTyp: Tipo de documento, Referenciado de TipoDocumento
            :userNatIdNum (String): Numero de documento.
            :grupo: Grupo de usuarios. Referenciado de Group
            :user: Usuario. Referenciado de User
            :contrasena (String): Contraseña
    """

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        app_label = 'LabModule'
        permissions = permissions_user

    nombre_usuario = models.CharField(
            verbose_name = _('Nombre de Usuario'),
            max_length = 255,
            validators = [
                RegexValidator(
                        regex = USERNAME_REGEX,
                        message = _('El nombre de usuario debe ser alfanúmerico o contener los siguientes: ". - _" '),
                        code = 'invalid_username'
                )],
            unique = True,
    )
    correo_electronico = models.EmailField(
            verbose_name = _('Correo Electrónico'),
            max_length = 255,
            validators = [
                RegexValidator(
                        regex = USERMAIL_REGEX,
                        message = _(
                                'El correo eletrónico debe ser alfanúmerico o contener los siguientes: ". @ + - _" '),
                        code = 'invalid_email'
                )],
            unique = True,
    )
    codigo_usuario = models.CharField(
            verbose_name = _("Código de Usuario"),
            max_length = 20,
            validators = [
                RegexValidator(
                        regex = USERCODE_REGEX,
                        message = _('El código de usuario debe ser alfanúmerico.'),
                        code = 'invalid_usercode'
                )],
            default = '',
            unique = True,
    )
    nombres = models.CharField(
            max_length = 30,
            default = '',
            verbose_name = _('Nombres')
    )
    apellidos = models.CharField(
            max_length = 30,
            default = '',
            verbose_name = _('Apellidos')
    )
    telefono = models.CharField(
            max_length = 20,
            default = '',
            verbose_name = _('Teléfono')
    )
    userNatIdTyp = models.ForeignKey(
            TipoDocumento,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = _('Tipo Identificación'),
            related_name = '%(app_label)s_%(class)s_related'
    )
    userNatIdNum = models.CharField(
            max_length = 15,
            default = '',
            verbose_name = _('Número de Identificación')
    )
    grupo = models.ForeignKey(
            Group,
            on_delete = models.CASCADE,
            related_name = '%(app_label)s_%(class)s_related',
            verbose_name = 'Grupo',
            null = False,
    )
    user = models.OneToOneField(
            User,
            on_delete = models.CASCADE,
            related_name = '%(app_label)s_%(class)s_related'
    )
    contrasena = models.CharField(
            max_length = 15,
            verbose_name = _('Contraseña')
    )

    def __unicode__(self):
        return self.user.username

    def nombre_completo(self):
        return self.nombres + " " + self.apellidos
