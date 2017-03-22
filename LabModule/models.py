# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

from .utils import code_generator

# Create your models here.


USERNAME_REGEX = '^[a-zA-Z0-9.-_]*$'
USERMAIL_REGEX = '^[a-zA-Z0-9.@-_]*$'
USERCODE_REGEX = '^[a-zA-Z0-9]*$'


class AccountRole(models.Model):
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    userRoleName = models.CharField(max_length=50, default='', verbose_name='Cargo')

    def __unicode__(self):
        return self.userRoleName


class DocumentIDType(models.Model):
    class Meta:
        verbose_name = 'Tipo Identificación'
        verbose_name_plural = 'Tipos de Indentificación'

    IdTypeName = models.CharField(max_length=2, default='', verbose_name='Nombre Tipo Identificación')
    IdTypeDesc = models.CharField(max_length=100, default='', verbose_name='Descripción Tipo Identificación')

    def __unicode__(self):
        return self.IdTypeName


class LabUserManager(BaseUserManager):
    def create_user(self, username, email, user_code, first_name, last_name, user_phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            user_code=user_code,
            first_name=first_name,
            last_name=last_name,
            user_phone=user_phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, user_code, first_name, last_name, user_phone, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            user_code,
            first_name,
            last_name,
            user_phone,
            password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class LabUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Nombre de Usuario',
        max_length=255,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='El nombre de usuario debe ser alfanúmerico o contener los siguientes: ". - _" ',
                code='invalid_username'
            )],
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Correo Electrónico',
        max_length=255,
        validators=[
            RegexValidator(
                regex=USERMAIL_REGEX,
                message='El correo eletrónico debe ser alfanúmerico o contener los siguientes: ". @ + - _" ',
                code='invalid_email'
            )],
        unique=True,
    )
    user_code = models.CharField(
        verbose_name="Código de Usuario",
        max_length=20,
        validators=[
            RegexValidator(
                regex=USERCODE_REGEX,
                message='El código de usuario debe ser alfanúmerico.',
                code='invalid_usercode'
            )],
        default='',
        unique=True,
    )
    first_name = models.CharField(
        max_length=50,
        default='',
        verbose_name='Nombres'
    )
    last_name = models.CharField(
        max_length=50,
        default='',
        verbose_name='Apellidos'
    )
    user_phone = models.CharField(
        max_length=20,
        default='',
        verbose_name='Teléfono'
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = LabUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_code', 'first_name', 'last_name', 'user_phone', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(ActivationProfile, self).save(*args, **kwargs)


def post_save_activation_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # send email
        print('Esto debería ejecutarse cada vez de registro un puto')


post_save.connect(post_save_activation_receiver, sender=ActivationProfile)


class AccountProfile(models.Model):
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    userRoleName = models.CharField(
        max_length=20,
        default='',
        verbose_name='Cargo',
        editable=False
    )
    userRole = models.ForeignKey(
        AccountRole,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Cargo'
    )
    userNatIdTypName = models.CharField(
        max_length=20, default='',
        verbose_name='Tipo Identificación',
        editable=False
    )
    userNatIdTyp = models.ForeignKey(
        DocumentIDType,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Tipo Identificación'
    )
    userNatIdNum = models.CharField(
        max_length=15,
        default='',
        verbose_name='Número de Identificación'
    )

    def __unicode__(self):
        return self.user.username


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            AccountProfile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class LaboratorioProfile(models.Model):
    """Representación del laboratorio
        Se encarga de:
            * Definir un laboratorio y los campos significativos
            * Permite guardar en la base de datos el laboratorio.

Atributos:
    :nombre (String): Nombre del laboratorio. Máxima longitud de 100 caracteres. No puede ser nulo
    :id (String): Id del laboratorio. Identificación del laboratorio, campo unico, máxima longitud de 100 caracteres.
    :numX (Integer): Cantidad de columnas que tiene el laboratorio para almacenar máquinas. Por defecto 10.
    :numY (Integer): Cantidad de filas que tiene el laboratorio para alamacenar máquinas. Por defecto 10.

    """

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        permissions = (
            ('can_addLab', 'laboratorio||agregar'),
            ('can_edditLab', 'laboratorio||editar'),
        )

    nombre = models.CharField(max_length=100, default='', verbose_name="Nombre", null=False)
    id = models.CharField(max_length=100, default='', verbose_name="Identificación", null=False, primary_key=True)
    numX = models.PositiveIntegerField(verbose_name="Cantidad de filas", null=False, default=10)
    numY = models.PositiveIntegerField(verbose_name="Cantidad de columnas", null=False, default=10)

    def __unicode__(self):
        return self.id + " " + self.nombre


class MaquinaProfile(models.Model):
    """Representación de una máquina.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la máquina

Atributos:
    :nombre (String): Nombre de la máquina, máxima longitud 100 caracteres, no puede ser nulo.
    :descripcion (String): Descripción de la máquina,  máxima longitud 1000 caracteres, no puede ser nulo.
    :imagen (ImafeField): Imágen de la máquina,  default='images/image-not-found.jpg'.
    :idSistema (String): Identificación del laboratorio, máxima longitud de 20 caracteres.
    :con_reserva (boolean): Dice si es necesario aprobar la máquina para ser reservada. Por defecto verdadero
    :activa (boolean): Dice si la máquina se puede solicitar. Por defecto verdadero

    """

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
    idSistema = models.CharField(max_length=20, default='', verbose_name="Identificación", null=False, primary_key=True)
    con_reserva = models.BooleanField(default=True, verbose_name="Reservable")
    activa = models.BooleanField(default=True, verbose_name="Activa")

    def __str__(self):
        return self.idSistema + " " + self.nombre

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})


class MaquinaEnLab(models.Model):
    """Relación entre :class:`MaquinaProfile` y :class:`LaboratorioProfile`
        Se encarga de:
            * Definir la posición del laboratorio en que la máquina esta guardada
            * Permite guardar en la base de datos esta relación

Atributos:
    :idLaboratorio (String): Id del laboratorio en el que la máquina esta guardada.
    :idMaquina (String): Id de la máquina que esta guaradada
    :xPos (Integer): Posición x en la que la máquina esta guardada. No puede ser nulo, por defecto 0.
    :yPos (Integer): Posición y en la que la máquina esta guardada. No puede sr nulo, por defecto 0.


    """

    class Meta:
        verbose_name = "Máquina en laboratorio"
        verbose_name_plural = 'Máquinas en laboratorio'

    idLaboratorio = models.ForeignKey(LaboratorioProfile, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name="Laboratorio")
    idMaquina = models.OneToOneField(MaquinaProfile, blank=False, null=False, on_delete=models.CASCADE,
                                     verbose_name="Máquina", primary_key=True)
    xPos = models.PositiveIntegerField(verbose_name="Posición x", null=False, default=0)
    yPos = models.PositiveIntegerField(verbose_name="Posición y", null=False, default=0)

    def __unicode__(self):
        return str(self.xPos) + "," + str(self.yPos)


class LugarAlmacenamiento(models.Model):
    """Representación de un lugar de almacenamiento.
            Se encarga de:
                * Definir las restricciónes basicas de los campos
                * Permite guardar en la base de datos el lugar de almacenamiento

Atributos:
    :nombre (String): Nombre del lugar de almacenamiento.
    :descripcion (String): Descripción del lugar de almacenamiento.
    :bandejasOcupadas (Integer): Bandejas ocupadas por el lugar de almacenamiento.
    :capacidad (Integer): Capacidad del lugar de almacenamiento.
    :temperatura (Decimal): Temperatura del lugar de almacenamiento.
    :estado (String): Estado del lugar de almacenamiento.
    :imagen (ImafeField): Imágen de lugar de almacenamiento,  default='images/image-not-found.jpg'.
    :peso (Decimal): Peso soportado por el lugar de almacenamiento.
    :tamano (Decimal): Tamaño del lugar de almacenamiento.

    """

    class Meta:
        verbose_name = 'Lugar Almacenamiento'
        verbose_name_plural = 'Lugares de Almacenamiento'

    nombre = models.CharField(max_length=100, default='', verbose_name='Nombre')
    descripcion = models.TextField(max_length=1000, default='', verbose_name="Descripcion")
    bandejasOcupadas = models.IntegerField(verbose_name="Bandejas Ocupadas", null=True)
    capacidad = models.IntegerField(verbose_name="Capacidad")
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temperatura")
    estado = models.CharField(max_length=100, default='', verbose_name='Estado', null=True)
    imagen = models.ImageField(upload_to='images', null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    tamano = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tamaño")


class LugarAlmacenamientoEnLab(models.Model):
    """Relación entre :class:`LugarAlmacenamiento` y :class:`LaboratorioProfile`
         Se encarga de:
             * Definir la posición del lugar Almacenamiento en donde esta guardada
             * Permite guardar en la base de datos esta relación

Atributos:
    :idLaboratorio (String): Id del laboratorio.
    :idLugar (String): Id del lugar Almacenamiento
    :xPos (Integer): Posición x en la que el lugar Almacenamiento esta guardado.
    :yPos (Integer): Posición y en la que el lugar Almacenamiento esta guardado.


     """

    class Meta:
        verbose_name = "Lugar almacenamiento en laboratorio"
        verbose_name_plural = 'Lugar almacenamiento en laboratorio'

    idLaboratorio = models.ForeignKey(LaboratorioProfile, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name="Laboratorio")
    idLugar = models.OneToOneField(LugarAlmacenamiento, blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="Lugar Almacenamiento", primary_key=True)
    posX = models.PositiveIntegerField(verbose_name="Posición x")
    posY = models.PositiveIntegerField(verbose_name="Posición y")

    def __unicode__(self):
        return str(self.posX) + "," + str(self.posY)


class Protocolo(models.Model):
    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'

    nombre = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre protocolo")
    descripcion = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del protocolo")
    objetivo = models.TextField(max_length=200, blank=False, null=True, verbose_name="Objetivo del protocolo")


class Paso(models.Model):
    class Meta:
        verbose_name = 'Paso'
        verbose_name_plural = 'Pasos'

    nombre = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre paso")
    descripcion = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del paso")
    protocolo = models.ForeignKey(Protocolo, blank=False, null=True,
                                  verbose_name="Seleccion de Protocolo")


class Muestra(models.Model):
    class Meta:
        verbose_name = 'Muestra'
        verbose_name_plural = 'Muestras'

    nombre = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre de la muestra")
    descripcion = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion de la muestra")
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso")
    volumen = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Volumen")
    cantidadInicial = models.IntegerField(blank=False, null=True,
                                          verbose_name="Cantidad inicial de la muestra")
    masa = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="Masa")
    estado = models.CharField(max_length=30, blank=False, null=True, verbose_name="Estado de la muestra")
    controlado = models.BooleanField(blank=False, verbose_name="Muestra controlada")
    cantidadActual = models.IntegerField(blank=False, null=True, verbose_name="Cantidad actual de la muestra")
    imagen = models.ImageField(upload_to='images', verbose_name="Imagen", default='images/image-not-found.jpg')
    unidad = models.CharField(max_length=50, blank=False, null=True, verbose_name="Unidad de medida")

    def __unicode__(self):
        return 'Muestra: ' + str(self.nombre)


class Bandeja(models.Model):
    """Representación de una bandeja del lugar de almacenamiento.
            Se encarga de:
                * Definir las restricciónes basicas de los campos
                * Permite guardar en la base de datos la bandeja del lugar de almacenamiento

Atributos:
    :tamano (String): Tamaño de la bandeja del lugar de almacenamiento.
    :cantidad (Integer): Cantidad de la bandeja del lugar de almacenamiento.
    :libre (Decimal): Indica si esta libre la bandeja del lugar de almacenamiento.
    :muestra (String): Relación con la entidad muestra.
    :lugarAlmacenamiento (Decimal): Relación con la entidad lugar de almacenamiento.
    """

    class Meta:
        verbose_name = 'Bandeja'
        verbose_name_plural = 'Bandejas'

    tamano = models.CharField(max_length=100, default='', verbose_name='Tamaño Bandeja', null=True)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    libre = models.BooleanField(blank=False, default=True, verbose_name="Libre")
    muestra = models.ForeignKey(Muestra, blank=False, null=True,
                                verbose_name="Seleccion de muestra")
    lugarAlmacenamiento = models.ForeignKey(LugarAlmacenamiento, blank=False, null=True, on_delete=models.CASCADE,
                                            verbose_name="Seleccion de Lugar almacenamiento")


class Solicitud(models.Model):
    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        permissions = (
            ('can_solMuestra', 'muestra||solicitar'),
        )

    descripcion = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion de la solicitud")
    fechaInicial = models.DateField(blank=False, null=True, verbose_name="Fecha inicial")
    fechaFinal = models.DateField(blank=False, null=True, verbose_name="Fecha final")
    estado = models.CharField(max_length=30, blank=False, null=True, verbose_name="Estado solicitud")
    solicitante = models.CharField(max_length=50, blank=False, null=True, verbose_name="Quien solicito")
    aprobador = models.CharField(max_length=50, blank=False, null=True, verbose_name="Quien aprobo")
    fechaActual = models.DateField(blank=False, null=True, verbose_name="Fecha actual")
    paso = models.ForeignKey(Paso, blank=False, null=True,
                             verbose_name="Seleccion de Paso")


class MuestraSolicitud(models.Model):
    class Meta:
        verbose_name = 'Solicitud de Muestra'
        verbose_name_plural = 'Solicitudes de Muestra'
        permissions = (
            ('can_solMuestra', 'muestra||solicitar'),
        )

    solicitud = models.OneToOneField(Solicitud)
    muestra = models.ForeignKey(Muestra, blank=False, null=True,
                                verbose_name="Seleccion de Muestra")
    cantidad = models.IntegerField(blank=False, null=True, verbose_name="Cantidad de muestra")
    tipo = models.CharField(max_length=30, blank=False, null=True, verbose_name="Tipo solicitud")


class Projecto(models.Model):
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    nombre = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre proyecto")
    descripcion = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del proyecto")
    objetivo = models.TextField(max_length=200, blank=False, null=True, verbose_name="Objetivo del proyecto")
    lider = models.ForeignKey(AccountProfile, blank=False, null=True,
                              verbose_name="Seleccion lider", related_name="lider")
    asistentes = models.ManyToManyField(AccountProfile, related_name="asistentes")
    activo = models.BooleanField(blank=False, null=False, default=True)


class Experimento(models.Model):
    class Meta:
        verbose_name = 'Experimento'
        verbose_name_plural = 'Experimentos'

    nombre = models.CharField(max_length=50, blank=False, null=True, verbose_name="Nombre expermento")
    descripcion = models.TextField(max_length=200, blank=False, null=True, verbose_name="Descripcion del experimento")
    objetivo = models.TextField(max_length=200, blank=False, null=True, verbose_name="Objetivo del experimento")
    projecto = models.ForeignKey(Projecto, blank=False, null=True, on_delete=models.CASCADE,
                                 verbose_name="Seleccion de Proyecto", related_name="proyecto")
    protocolos = models.ManyToManyField(Protocolo, related_name="experimento")
