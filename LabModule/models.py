# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

# Create your models here.

USERNAME_REGEX = '^[a-zA-Z0-9.-_]*$'
USERMAIL_REGEX = '^[a-zA-Z0-9.@-_]*$'
USERCODE_REGEX = '^[a-zA-Z0-9]*$'


class TipoDocumento(models.Model):
    """Representación del Tipos de Documento
        Se encarga de:
            * Definir los tipos de documentos a manejar en el sistema

        Atributos:
            :nombre_corto (String): Nnemotecnico Tipo Documento. Maxima longitud 5 caraceres.
            :descripcion (String): Descripcion Tipo Documento. Maxima longitud 100 caraceres.
    """

    class Meta:
        verbose_name = 'Tipo Identificación'
        verbose_name_plural = 'Tipos de Indentificación'

    nombre_corto = models.CharField(
        max_length=5,
        default='',
        verbose_name='Abreviación Tipo Identificación'
    )
    descripcion = models.CharField(
        max_length=100,
        default='',
        verbose_name='Descripción Tipo Identificación'
    )

    def __unicode__(self):
        return self.nombre_corto


class Usuario(models.Model):
    """Representación de Usuarios
        Se encarga de:
            * Definir los usuarios y sus atributos

        Atributos:
            :nombre_usuario (String): Nombre de usuario. Maxima longitud 255 caraceres, unico.
            :correo_electronico (String): Correo electronico. Maxima longitud 255 caraceres, unico.
            :codigo_usuario (String): Codigo de usuario. Maxima longitud 20 caraceres, unico.
            :nombres (String): Nombres. Maxima longitud 50 caraceres.
            :apellidos (String): Apellidos. Maxima longitud 50 caraceres.
            :telefono (String): Teléfono. Maxima longitud 20 caraceres.
            :userNatIdTyp: Tipo de documento, Referenciado de TipoDocumento
            :userNatIdNum (String): Numero de documento.
            :grupo: Grupo de usuarios. Referenciado de Group
            :user: Usuario. Referenciado de User
            :contrasena (String): Contraseña
    """

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        permissions = (
            ('can_addUser', 'usuario||agregar'),
        )

    nombre_usuario = models.CharField(
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
    correo_electronico = models.EmailField(
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
    codigo_usuario = models.CharField(
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
    nombres = models.CharField(
        max_length=30,
        default='',
        verbose_name='Nombres'
    )
    apellidos = models.CharField(
        max_length=30,
        default='',
        verbose_name='Apellidos'
    )
    telefono = models.CharField(
        max_length=20,
        default='',
        verbose_name='Teléfono'
    )
    userNatIdTyp = models.ForeignKey(
        TipoDocumento,
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
    grupo = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Grupo',
        null=False
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    contrasena = models.CharField(
        max_length=15,
        verbose_name='Contraseña'
    )

    def __unicode__(self):
        return self.user.username


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

        Permisos:
            :can_addLab: Permite agregar Laboratorios
            :can_edditLab: Permite modificar Laboratorios
    """

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        permissions = (
            ('can_addLab', 'laboratorio||agregar'),
            ('can_edditLab', 'laboratorio||editar'),
        )

    nombre = models.CharField(
        max_length=100,
        default='',
        verbose_name="Nombre",
        null=False
    )
    id = models.CharField(
        max_length=100,
        default='',
        verbose_name="Identificación",
        null=False,
        primary_key=True
    )
    numX = models.PositiveIntegerField(
        verbose_name="Cantidad de filas",
        null=False,
        default=10
    )
    numY = models.PositiveIntegerField(
        verbose_name="Cantidad de columnas",
        null=False,
        default=10
    )

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

        Permisos:
            :can_addMachine: Permite agregar Maquinas
            :can_edditMachine: Permite modificar Maquinas
            :can_viewMachine: Permite modificar Maquinas
            """

    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = 'Máquinas'
        permissions = (
            ('can_addMachine', 'maquina||agregar'),
            ('can_edditMachine', 'maquina||editar'),
            ('can_viewMachine', 'maquina||ver')
        )

    nombre = models.CharField(
        max_length=100,
        default='',
        verbose_name="Nombre",
        null=False
    )
    descripcion = models.CharField(
        max_length=1000,
        default='',
        verbose_name="Descripción",
        null=True
    )
    imagen = models.ImageField(
        upload_to='images',
        verbose_name="Imagen",
        default='images/image-not-found.jpg'
    )
    idSistema = models.CharField(
        max_length=20,
        default='',
        verbose_name="Identificación",
        null=False,
        primary_key=True
    )
    con_reserva = models.BooleanField(
        default=True,
        verbose_name="Reservable"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

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

    idLaboratorio = models.ForeignKey(
        LaboratorioProfile,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Laboratorio"
    )
    idMaquina = models.OneToOneField(
        MaquinaProfile,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Máquina",
        primary_key=True
    )
    xPos = models.PositiveIntegerField(
        verbose_name="Posición x",
        null=False,
        default=0
    )
    yPos = models.PositiveIntegerField(
        verbose_name="Posición y",
        null=False,
        default=0
    )

    def __unicode__(self):
        return self.idLaboratorio.id + ":" + str(self.xPos) + "," + str(self.yPos)


class LugarAlmacenamiento(models.Model):
    """Representación de un lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos el lugar de almacenamiento

        Atributos:
            :nombre (String): Nombre del lugar de almacenamiento.
            :descripcion (String): Descripción del lugar de almacenamiento
            :capacidad (Integer): Capacidad del lugar de almacenamiento.
            :temperatura (Decimal): Temperatura del lugar de almacenamiento.
            :estado (String): Estado del lugar de almacenamiento.
            :imagen (ImafeField): Imágen de lugar de almacenamiento,  default='images/image-not-found.jpg'.
        Permisos:
            :can_addStorage: Permite agregar Almacenamientos
            :can_editStorage: Permite modificar Almacenamientos
            :can_viewStorage: Permite ver Almacenamientos
    """

    class Meta:
        verbose_name = 'Lugar Almacenamiento'
        verbose_name_plural = 'Lugares de Almacenamiento'
        permissions = (
            ('can_addStorage', 'almacenamiento||agregar'),
            ('can_editStorage', 'almacenamiento||editar'),
            ('can_viewStorage', 'almacenamiento||ver')
        )

    nombre = models.CharField(
        max_length=100,
        default='',
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        max_length=1000,
        default='',
        verbose_name="Descripcion"
    )

    capacidad = models.IntegerField(
        verbose_name="Capacidad"
    )
    temperatura = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Temperatura"
    )
    estado = models.CharField(
        max_length=100,
        default='',
        verbose_name='Estado',
        null=True
    )
    imagen = models.ImageField(
        upload_to='images',
        verbose_name="Imagen",
        default='images/image-not-found.jpg'
    )


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

    idLaboratorio = models.ForeignKey(
        LaboratorioProfile,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Laboratorio"
    )
    idLugar = models.OneToOneField(
        LugarAlmacenamiento,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Lugar Almacenamiento",
        primary_key=True
    )
    posX = models.PositiveIntegerField(
        verbose_name="Posición x"
    )
    posY = models.PositiveIntegerField(
        verbose_name="Posición y"
    )

    def __unicode__(self):
        return str(self.posX) + "," + str(self.posY)


class Protocolo(models.Model):
    """Representacion de Protocolos
         Se encarga de:
             * Definir las caracteristicas de un protocolo
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre del protocolo.
             :descripcion (String): Descripcion del protocolo
             :objetivo (String): Objetivo del protocolo
        Permisos:
            :can_addProtocol: Permite agregar protocolo
            :can_editProtocol: Permite modificar protocolo
            :can_viewProtocol: Permite ver protocolo
      """

    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'
        permissions = (
            ('can_addProtocol', 'protocolo||agregar'),
            ('can_editProtocol', 'protocolo||editar'),
            ('can_viewProtocol', 'protocolo||ver')
        )

    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Nombre protocolo"
    )
    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Descripcion del protocolo"
    )
    objetivo = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Objetivo del protocolo"
    )


class Paso(models.Model):
    """Representacion de Paso
         Se encarga de:
             * Definir las caracteristicas de un paso
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre del paso.
             :descripcion (String): Descripcion del paso
             :protocolo (Relacion): Seleccion de Protocolo
        Permisos:
            :can_addStep: Permite agregar paso
            :can_editStep: Permite modificar paso
            :can_viewStep: Permite ver paso
      """

    class Meta:
        verbose_name = 'Paso'
        verbose_name_plural = 'Pasos'
        permissions = (
            ('can_addStep', 'paso||agregar'),
            ('can_editStep', 'paso||editar'),
            ('can_viewStep', 'paso||ver')
        )

    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Nombre paso"
    )
    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Descripcion del paso"
    )
    protocolo = models.ForeignKey(
        Protocolo,
        blank=False,
        null=True,
        verbose_name="Seleccion de Protocolo"
    )


class Muestra(models.Model):
    """Representacion de Muestra
         Se encarga de:
             * Definir las caracteristicas de un muestra
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre de la muestra
             :descripcion (String): Descripcion de la muestra
             :peso (Numeric): Peso de la muestra
             :volumen (Numeric): Volumen de la muestra
             :cantidadInicial (Numeric): Cantidad inicial de la muestra
             :masa (Numeric): Masa de la muestra
             :activa (Boolean): Estado de disponibilidad de la muestra
             :controlado (Boolean): Estado de restriccion de la muestra
             :cantidadActual (Numeric): Cantidad actual de la muestra
             :imagen (Image): Imagen de la muestra
             :unidad (String): Unidad de medida de la muestra
        Permisos:
            :can_addSample: Permite agregar muestra
            :can_editSample: Permite modificar muestra
            :can_viewSample: Permite ver muestra
      """

    class Meta:
        verbose_name = 'Muestra'
        verbose_name_plural = 'Muestras'
        permissions = (
            ('can_addSample', 'muestra||agregar'),
            ('can_editSample', 'muestra||editar'),
            ('can_viewSample', 'muestra||ver')
        )

    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Nombre de la muestra"
    )
    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Descripcion de la muestra"
    )
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Peso"
    )
    volumen = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Volumen"
    )
    cantidadInicial = models.IntegerField(
        blank=False, null=True,
        verbose_name="Cantidad inicial de la muestra"
    )
    masa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        verbose_name="Masa"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    controlado = models.BooleanField(
        blank=False,
        verbose_name="Muestra controlada"
    )
    cantidadActual = models.IntegerField(
        blank=False,
        null=True,
        verbose_name="Cantidad actual de la muestra"
    )
    imagen = models.ImageField(
        upload_to='images',
        verbose_name="Imagen",
        default='images/image-not-found.jpg'
    )
    unidad = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Unidad de medida"
    )

    def __unicode__(self):
        return 'Muestra: ' + str(self.nombre)

    def calc_disp(self):
        bandejas = Bandeja.objects.filter(muestra=self)
        for bandeja in bandejas:
            if not bandeja.libre:
                return 'Si'
        return 'No'

    def calc_controled(self):
        if self.controlado:
            return 'Si'
        else:
            return 'No'


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

    tamano = models.CharField(
        max_length=100,
        default='',
        verbose_name='Tamaño Bandeja',
        null=True
    )
    cantidad = models.IntegerField(
        verbose_name="Cantidad"
    )
    libre = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="Libre"
    )
    muestra = models.ForeignKey(
        Muestra,
        blank=False,
        null=True,
        verbose_name="Seleccion de muestra"
    )
    lugarAlmacenamiento = models.ForeignKey(
        LugarAlmacenamiento,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Seleccion de Lugar almacenamiento"
    )


class Solicitud(models.Model):
    """Representación de una bandeja del lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la solicitud

        Atributos:
            :tamano (String): Tamaño de la bandeja del lugar de almacenamiento.
            :cantidad (Integer): Cantidad de la bandeja del lugar de almacenamiento.
            :libre (Decimal): Indica si esta libre la bandeja del lugar de almacenamiento.
            :muestra (String): Relación con la entidad muestra.
            :lugarAlmacenamiento (Decimal): Relación con la entidad lugar de almacenamiento.
    """

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Descripcion de la solicitud"
    )
    fechaInicial = models.DateField(
        blank=False,
        null=True,
        verbose_name="Fecha inicial",
        default=datetime.date.today
    )
    fechaFinal = models.DateField(
        blank=False,
        null=True,
        verbose_name="Fecha final",
        default=datetime.date.today
    )
    estado = models.CharField(
        max_length=30,
        blank=False,
        null=True,
        verbose_name="Estado solicitud"
    )
    solicitante = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Quien solicito"
    )
    aprobador = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Quien aprobo"
    )
    fechaActual = models.DateField(
        blank=False,
        null=True,
        verbose_name="Fecha actual",
        default=datetime.date.today
    )
    paso = models.ForeignKey(
        Paso,
        blank=False,
        null=True,
        verbose_name="Seleccion de Paso"
    )


class MuestraSolicitud(models.Model):
    """Relación entre :class:`Muestra` y :class:`Solicitud` Detalle de solicitud
        Se encarga de:
            * Definir la relacion entre solicitud y muestras solicitadas
            * Permite guardar en la base de datos el detalle de una solicitud

        Atributos:
            :solicitud (Decimal): Id solicitud.
            :muestra (Decimal): Seleccion de Muestra
            :cantidad (Integer): Cantidad de muestra.
            :tipo (String):Tipo solicitud.
        Permisos:
            :can_solMuestra: Permite solicitar muestra
         """

    class Meta:
        verbose_name = 'Solicitud de Muestra'
        verbose_name_plural = 'Solicitudes de Muestra'
        permissions = (
            ('can_solMuestra', 'muestra||solicitar'),
        )

    solicitud = models.OneToOneField(Solicitud)
    muestra = models.ForeignKey(
        Muestra,
        blank=False,
        null=True,
        verbose_name="Seleccion de Muestra"
    )
    cantidad = models.IntegerField(
        blank=False,
        null=True,
        verbose_name="Cantidad de muestra"
    )
    tipo = models.CharField(
        max_length=30,
        blank=False,
        null=True,
        verbose_name="Tipo solicitud"
    )


class MaquinaSolicitud(models.Model):
    class Meta:
        verbose_name = 'Solicitud de Maquina'
        verbose_name_plural = 'Solicitudes de Maquina'
        permissions = (
            ('can_solMaquina', 'maquina||solicitar'),
        )

    solicitud = models.OneToOneField(Solicitud)
    maquina = models.ForeignKey(
        MaquinaProfile,
        blank=False,
        null=True,
        verbose_name="Seleccion de Maquina"
    )


class Projecto(models.Model):
    """Representación de un proyecto.
        Se encarga de:
            * Definir las caracteristicas de un proyecto
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos esta entidad

        Atributos:
            :nombre (String): Nombre proyecto
            :descripcion (String): Descripcion del proyecto.
            :objetivo (String): Objetivo del proyecto
            :lider (Decimal): Seleccion lider
            :asistentes (Object): Lista de asistentes
            :activo (Boolean): Estado de actividad del proyecto
        Permisos:
            :can_addProject: Permite agregar Proyecto
            :can_editProject: Permite modificar Proyecto
            :can_viewProject: Permite ver Proyecto
    """

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        permissions = (
            ('can_addProject', 'proyecto||agregar'),
            ('can_editProject', 'proyecto||editar'),
            ('can_viewProject', 'proyecto||ver')
        )

    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Nombre proyecto"
    )
    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Descripcion del proyecto"
    )
    objetivo = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Objetivo del proyecto"
    )
    lider = models.ForeignKey(
        Usuario,
        blank=False,
        null=True,
        verbose_name="Seleccion lider",
        related_name="lider"
    )
    asistentes = models.ManyToManyField(
        Usuario,
        related_name="asistentes"
    )
    activo = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        verbose_name='Estado de actividad del proyecto'
    )


class Experimento(models.Model):
    """Representación de un experimento.
        Se encarga de:
            * Definir las caracteristicas de un experimento
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos esta entidad

        Atributos:
            :nombre (String): Nombre expermento
            :descripcion (String): Descripcion del experimento.
            :objetivo (String): Objetivo del experimento
            :projecto (Decimal): Seleccion de Proyecto
            :protocolos (Object): Lista de protocolos
        Permisos:
            :can_addExperiment: Permite agregar experimento
            :can_editExperiment: Permite modificar experimento
            :can_viewExperiment: Permite ver experimento
    """

    class Meta:
        verbose_name = 'Experimento'
        verbose_name_plural = 'Experimentos'
        permissions = (
            ('can_addExperiment', 'experimento||agregar'),
            ('can_editExperiment', 'experimento||editar'),
            ('can_viewExperiment', 'experimento||ver')
        )

    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=True,
        verbose_name="Nombre expermento"
    )
    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Descripcion del experimento"
    )
    objetivo = models.TextField(
        max_length=200,
        blank=False,
        null=True,
        verbose_name="Objetivo del experimento"
    )
    projecto = models.ForeignKey(
        Projecto,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Seleccion de Proyecto",
        related_name="proyecto"
    )
    protocolos = models.ManyToManyField(
        Protocolo,
        related_name="experimento"
    )
