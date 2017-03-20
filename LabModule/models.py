# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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


class LaboratorioProfile(models.Model):
    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        permissions = (
            ('can_addLab', 'laboratorio||agregar'),
            ('can_edditLab', 'laboratorio||editar'),
        )

    nombre = models.CharField(max_length=100, default='', verbose_name="Nombre", null=False)
    id = models.CharField(max_length=100, default='', verbose_name="Identificación", null=False, primary_key=True)
    numX=models.PositiveIntegerField(verbose_name="Cantidad de filas", null=False,default=10);
    numY = models.PositiveIntegerField(verbose_name="Cantidad de columnas", null=False,default=10);
    def __unicode__(self):
        return self.id+" "+self.nombre


class MaquinaProfile(models.Model):
    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = 'Máquinas'
        permissions = (
            ('can_addMachine', 'maquina||agregar'),
            ('can_edditMachine', 'maquina||editar'),
        )

    nombre = models.CharField(max_length=100, default='', verbose_name="Nombre", null=False)
    descripcion = models.CharField(max_length=1000, default='', verbose_name="Descripción", null=True)
    imagen = models.ImageField(upload_to='images', verbose_name="Imagen", default='images/image-not-found.jpg')
    idSistema = models.CharField(max_length=20, default='', verbose_name="Identificación", null=False)
    con_reserva = models.BooleanField(default=True, verbose_name="Reservable")
    activa = models.BooleanField(default=True, verbose_name="Activa")
    # Esto se reemplazara eventualmente con una llave foranea
    laboratorio = models.ForeignKey(LaboratorioProfile, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name="Seleccionar Laboratorio")
    xPos = models.IntegerField(verbose_name="Posición x", null=False,default=0)
    yPos = models.IntegerField(verbose_name="Posición y", null=False,default=0)


    def __unicode__(self):
        return self.idSistema+" "+self.nombre

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

class MaquinaEnLab(models.Model):
    class Meta:
        verbose_name="Máquina en laboratorio"
        verbose_name_plural = 'Máquinas en laboratorio'
    idLaboratorio=models.ForeignKey(LaboratorioProfile, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name="Laboratorio")
    idMaquina=models.ForeignKey(MaquinaProfile, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name="Máquina")
    xPos = models.IntegerField(verbose_name="Posición x", null=False,default=0)
    yPos = models.IntegerField(verbose_name="Posición y", null=False,default=0)


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


class Bandeja(models.Model):
    class Meta:
        verbose_name = 'Bandeja'
        verbose_name_plural = 'Bandejas'

    tamano = models.CharField(max_length=100, default='', verbose_name='Tamaño Bandeja', null=True)
    cantidad = models.IntegerField(verbose_name="Cantidad")

    lugarAlmacenamiento = models.ForeignKey(LugarAlmacenamiento, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name="Seleccion de Lugar almacenamiento")

class Protocol(models.Model):
    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'

    name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre protocolo")
    description = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del protocolo")
    objetive = models.TextField(max_length=200, blank=False, null=True, verbose_name="Objetivo del protocolo")


class Step(models.Model):
    class Meta:
        verbose_name = 'Paso'
        verbose_name_plural = 'Pasos'

    name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre paso")
    description = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del paso")
    protocol = models.ForeignKey(Protocol, blank=False, null=True,
                                  verbose_name="Seleccion de Protocolo")



class Sample(models.Model):
    class Meta:
        verbose_name = 'Muestra'
        verbose_name_plural = 'Muestras'

    name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre de la muestra")
    description = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion de la muestra")
    weight = models.CharField(max_length=10, blank=False, null=True, verbose_name="Peso de la muestra")
    volume = models.CharField(max_length=10, blank=False, null=True, verbose_name="Volumen de la muestra")
    initialQuantity = models.IntegerField( blank=False, null=True,
                                          verbose_name="Cantidad inicial de la muestra")
    mass = models.CharField(max_length=10, blank=False, null=True, verbose_name="Masa de la muestra")
    state = models.CharField(max_length=30, blank=False, null=True, verbose_name="Estado de la muestra")
    controled = models.BooleanField(blank=False, verbose_name="Muestra controlada")
    actualQuantity = models.IntegerField(blank=False, null=True, verbose_name="Cantidad actual de la muestra")
    imageField= models.ImageField(upload_to='images', verbose_name="Imagen", default='images/image-not-found.jpg')
    unity=models.CharField(max_length=50, blank=False, null=True, verbose_name="Unidad de medida")

    def __unicode__(self):
        return 'Muestra: ' + str(self.name)


class Tray(models.Model):
    class Meta:
        verbose_name = 'Bandeja2'
        verbose_name_plural = 'Bandejas2'
    sample= models.ForeignKey(Sample, blank=False, null=True,
                             verbose_name="Seleccion de muestra")
    empty=models.BooleanField(blank=False, verbose_name="Libre")



class Request(models.Model):
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    description = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion de la solicitud")
    initialDate = models.DateField(blank=False, null=True, verbose_name="Fecha inicial")
    finalDate = models.DateField(blank=False, null=True, verbose_name="Fecha final")
    state = models.CharField(max_length=30, blank=False, null=True, verbose_name="Estado solicitud")
    applicant = models.CharField(max_length=50, blank=False, null=True, verbose_name="Quien solicito")
    approver = models.CharField(max_length=50, blank=False, null=True, verbose_name="Quien aprobo")
    actualDate = models.DateField(blank=False, null=True, verbose_name="Fecha actual")
    step = models.ForeignKey(Step, blank=False, null=True,
                             verbose_name="Seleccion de Paso")


class SampleRequest(models.Model):
    class Meta:
        verbose_name = 'Solicitud de Muestra'
        verbose_name_plural = 'Solicitudes de Muestra'

    request = models.OneToOneField(Request)
    sample = models.ForeignKey(Sample, blank=False, null=True,
                                verbose_name="Seleccion de Muestra")
    quantity = models.IntegerField(blank=False, null=True, verbose_name="Cantidad de muestra")
    type = models.CharField(max_length=30, blank=False, null=True, verbose_name="Tipo solicitud")



class Project(models.Model):
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre proyecto")
    description = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del proyecto")
    objetive = models.TextField(max_length=200, blank=False, null=True, verbose_name="Objetivo del proyecto")
    leader = models.ForeignKey(UserProfile, blank=False, null=True,
                              verbose_name="Seleccion lider", related_name="lider")
    assistants = models.ManyToManyField(UserProfile, related_name="assistants")
    active= models.BooleanField(blank=False,null=False,default=True)




class Experiment(models.Model):
    class Meta:
        verbose_name = 'Experimento'
        verbose_name_plural = 'Experimentos'

    name = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre expermento")
    description = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del experimento")
    objetive = models.TextField(max_length=200, blank=False, null=True, verbose_name="Objetivo del experimento")
    project = models.ForeignKey(Project, blank=False, null=True, on_delete=models.CASCADE,
                                 verbose_name="Seleccion de Proyecto", related_name="proyect")
    protocols = models.ManyToManyField(Protocol, related_name="experiment")

