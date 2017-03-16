# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserRole(models.Model):
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    userRoleName = models.CharField(max_length=50, default='', verbose_name='Cargo')

    def __unicode__(self):
        return self.userRoleName


class IdType(models.Model):
    class Meta:
        verbose_name = 'Tipo Identificación'
        verbose_name_plural = 'Tipos de Indentificación'

    IdTypeName = models.CharField(max_length=2, default='', verbose_name='Nombre Tipo Identificación')
    IdTypeDesc = models.CharField(max_length=100, default='', verbose_name='Descripción Tipo Identificación')

    def __unicode__(self):
        return self.IdTypeName


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    userCode = models.CharField(max_length=20, default='', verbose_name="Código")
    userRoleName = models.CharField(max_length=20, default='', verbose_name='Cargo', editable=False)
    userGivenName = models.CharField(max_length=50, default='', verbose_name='Nombres')
    userLastName = models.CharField(max_length=50, default='', verbose_name='Apellidos')
    userPhone = models.CharField(max_length=20, default='', verbose_name='Teléfono')
    userNatIdTypName = models.CharField(max_length=20, default='', verbose_name='Tipo Identificación', editable=False)
    userNatIdNum = models.CharField(max_length=15, default='', verbose_name='Número de Identificación')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    userRole = models.ForeignKey(UserRole, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Cargo')
    userNatIdTyp = models.ForeignKey(IdType, blank=False, null=False, on_delete=models.CASCADE,
                                     verbose_name='Tipo Identificación')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __unicode__(self):
        return self.user.username


class LugarAlmacenamiento(models.Model):
    class Meta:
        verbose_name = 'Lugar Almacenamiento'
        verbose_name_plural = 'Lugares de Almacenamiento'

    nombre = models.CharField(max_length=100, default='', verbose_name='Nombre')
    descripcion = models.TextField(max_length=1000, default='', verbose_name="Descripcion")
    bandejasOcupadas = models.IntegerField(verbose_name="Bandejas Ocupadas", null=True)
    capacidad = models.IntegerField(verbose_name="Capacidad")
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temperatura")
    posX = models.IntegerField(verbose_name="PosicionX")
    posY = models.IntegerField(verbose_name="PosicionY")
    estado = models.CharField(max_length=100, default='', verbose_name='Estado', null=True)
    tamanoBandeja = models.CharField(max_length=100, default='', verbose_name='Tamaño Bandeja', null=True)
    imagen = models.ImageField(upload_to='images', null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    tamano = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tamaño")
