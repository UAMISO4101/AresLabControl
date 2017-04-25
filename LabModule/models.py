# -*- coding: utf-8 -*-
from django.utils import timezone
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Max

# Create your models here.

USERNAME_REGEX = '^[a-zA-Z0-9.-_]*$'
USERMAIL_REGEX = '^[a-zA-Z0-9.@-_]*$'
USERCODE_REGEX = '^[a-zA-Z0-9]*$'

permissions_project = (
    ('can_addProject', 'proyecto||agregar'),
    ('can_editProject', 'proyecto||editar'),
    ('can_listProject', 'proyecto||listar'),
    ('can_viewProject', 'proyecto||ver'),
)

permissions_experiment = (
    ('can_addExperiment', 'experimento||agregar'),
    ('can_editExperiment', 'experimento||editar'),
    ('can_listExperiment', 'experimento||listar'),
    ('can_viewExperiment', 'experimento||ver'),
)

permissions_user = (
    ('can_addUser', 'usuario||agregar'),
    ('can_editUser', 'usuario||editar'),
    ('can_listUser', 'usuario||listar'),
    ('can_viewUser', 'usuario||ver'),
)

permissions_lab = (
    ('can_addLab', 'laboratorio||agregar'),
    ('can_editLab', 'laboratorio||editar'),
    ('can_listLab', 'laboratorio||listar'),
    ('can_viewLab', 'laboratorio||ver'),
)

permissions_machine = (
    ('can_addMachine', 'maquina||agregar'),
    ('can_editMachine', 'maquina||editar'),
    ('can_listMachine', 'maquina||listar'),
    ('can_viewMachine', 'maquina||ver'),
    ('can_requestMachine', 'maquina||solicitar'),
)

permissions_storage = (
    ('can_addStorage', 'almacenamiento||agregar'),
    ('can_editStorage', 'almacenamiento||editar'),
    ('can_listStorage', 'almacenamiento||listar'),
    ('can_viewStorage', 'almacenamiento||ver'),
    ('can_requestStorage', 'almacenamiento||solicitar'),
)

permissions_protocol = (
    ('can_addProtocol', 'protocolo||agregar'),
    ('can_editProtocol', 'protocolo||editar'),
    ('can_listProtocol', 'protocolo||listar'),
    ('can_viewProtocol', 'protocolo||ver'),
)

permissions_step = (
    ('can_addStep', 'paso||agregar'),
    ('can_editStep', 'paso||editar'),
    ('can_listStep', 'paso||listar'),
    ('can_viewStep', 'paso||ver'),
)

permissions_sample = (
    ('can_addSample', 'muestra||agregar'),
    ('can_editSample', 'muestra||editar'),
    ('can_listSample', 'muestra||listar'),
    ('can_viewSample', 'muestra||ver'),
    ('can_requestSample', 'muestra||solicitar'),
)

permissions_request = (
    ('can_listRequest', 'solicitud||listar'),
    ('can_viewRequest', 'solicitud||ver'),
    ('can_manageRequest', 'solicitud||admin'),
)

permissions_tray = (
    ('can_addTray', 'bandeja||agregar'),
    ('can_editTray', 'bandeja||editar'),
    ('can_listTray', 'bandeja||listar'),
    ('can_viewTray', 'bandeja||ver'),
)


class TipoDocumento(models.Model):
    """Representación del Tipos de Documento
        Se encarga de:
            * Definir los tipos de documentos a manejar en el sistema

        Atributos:
            :nombre_corto (String): Nnemotécnico Tipo Documento. Máxima longitud 5 caractéres.
            :descripcion (String): Descripción Tipo Documento. Máxima longitud 100 caractéres.
    """

    class Meta:
        verbose_name = _('Tipo Identificación')
        verbose_name_plural = _('Tipos de Indentificación')

    nombre_corto = models.CharField(
            max_length = 5,
            default = '',
            verbose_name = _('Abreviación Tipo Identificación')
    )
    descripcion = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _('Descripción Tipo Identificación')
    )

    def __unicode__(self):
        return self.nombre_corto


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
            verbose_name = _('Tipo Identificación')
    )
    userNatIdNum = models.CharField(
            max_length = 15,
            default = '',
            verbose_name = _('Número de Identificación')
    )
    grupo = models.ForeignKey(
            Group,
            on_delete = models.CASCADE,
            related_name = 'profile',
            verbose_name = 'Grupo',
            null = False
    )
    user = models.OneToOneField(
            User,
            on_delete = models.CASCADE,
            related_name = 'profile'
    )
    contrasena = models.CharField(
            max_length = 15,
            verbose_name = _('Contraseña')
    )

    def __unicode__(self):
        return self.user.username
    def nombre_completo(self):
        return self.nombres +" "+ self.apellidos

class LaboratorioProfile(models.Model):
    """Representación del laboratorio
        Se encarga de:
            * Definir un laboratorio y los campos significativos
            * Permite guardar en la base de datos el laboratorio.

        Atributos:
            :nombre (String): Nombre del laboratorio. Máxima longitud de 100 caractéres. No puede ser nulo
            :id (String): Id del laboratorio. Identificación del laboratorio, campo único, 
                          máxima longitud de 100 caractéres.
            :numX (Integer): Cantidad de columnas que tiene el laboratorio para almacenar máquinas. Por defecto 10.
            :numY (Integer): Cantidad de filas que tiene el laboratorio para alamacenar máquinas. Por defecto 10.

        Permisos:
            :can_addLab: Permite agregar Laboratorios
            :can_edditLab: Permite modificar Laboratorios
    """

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        permissions = permissions_lab

    nombre = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Nombre"),
            null = False
    )
    id = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Identificación"),
            null = False,
            primary_key = True
    )
    numX = models.PositiveIntegerField(
            verbose_name = _("Cantidad de Filas"),
            null = False,
            default = 10
    )
    numY = models.PositiveIntegerField(
            verbose_name = _("Cantidad de Columnas"),
            null = False,
            default = 10
    )

    def __unicode__(self):
        return self.id + " " + self.nombre


class MaquinaProfile(models.Model):
    """Representación de una máquina.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la máquina

        Atributos:
            :nombre (String): Nombre de la máquina, máxima longitud 100 caractéres, no puede ser nulo.
            :descripción (String): Descripción de la máquina,  máxima longitud 1000 caractéres, no puede ser nulo.
            :imagen (ImafeField): Imágen de la máquina,  default='images/image-not-found.jpg'.
            :idSistema (String): Identificación del laboratorio, máxima longitud de 20 caractéres.
            :con_reserva (boolean): Dice si es necesario aprobar la máquina para ser reservada. Por defecto verdadero
            :activa (boolean): Dice si la máquina se puede solicitar. Por defecto verdadero

        Permisos:
            :can_addMachine: Permite agregar maquinas
            :can_edditMachine: Permite modificar maquinas
            :can_viewMachine: Permite modificar maquinas
            """

    class Meta:
        verbose_name = _("Máquina")
        verbose_name_plural = _('Máquinas')
        permissions = permissions_machine

    nombre = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _("Nombre"),
            null = False
    )
    descripcion = models.CharField(
            max_length = 1000,
            default = '',
            verbose_name = _("Descripción"),
            null = True
    )
    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )
    idSistema = models.CharField(
            max_length = 20,
            default = '',
            verbose_name = _("Identificación"),
            null = False,
            primary_key = True
    )
    con_reserva = models.BooleanField(
            default = True,
            verbose_name = _("Reservable")
    )
    activa = models.BooleanField(
            default = True,
            verbose_name = _("Activa")
    )

    def __unicode__(self):
        return self.idSistema + " " + self.nombre

    def get_absolute_url(self):
        return reverse('author-detail', kwargs = {'pk': self.pk})


class MaquinaEnLab(models.Model):
    """Relación entre :class:`MaquinaProfile` y :class:`LaboratorioProfile`
        Se encarga de:
            * Definir la posición del laboratorio en que la máquina esta guardada
            * Permite guardar en la base de datos esta relación

        Atributos:
            :idLaboratorio (String): Id del laboratorio en el que la máquina esta guardada.
            :idMaquina (String): Id de la máquina que esta guaradada
            :posX (Integer): Posición x en la que la máquina esta guardada. No puede ser nulo, por defecto 0.
            :posY (Integer): Posición y en la que la máquina esta guardada. No puede sr nulo, por defecto 0.
    """

    class Meta:
        verbose_name = _("Máquina en Laboratorio")
        verbose_name_plural = _('Máquinas en Laboratorio')

    idLaboratorio = models.ForeignKey(
            LaboratorioProfile,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = "Laboratorio"
    )
    idMaquina = models.OneToOneField(
            MaquinaProfile,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = "Máquina",
            primary_key = True
    )
    posX = models.PositiveIntegerField(
            verbose_name = "Posición X",
            null = False,
            default = 0
    )
    posY = models.PositiveIntegerField(
            verbose_name = "Posición Y",
            null = False,
            default = 0
    )

    def __unicode__(self):
        return self.idLaboratorio.id + ":" + str(self.posX) + "," + str(self.posY)


class LugarAlmacenamiento(models.Model):
    """Representación de un lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos el lugar de almacenamiento

        Atributos:
            :nombre (String): Nombre del lugar de almacenamiento.
            :descripción (String): Descripción del lugar de almacenamiento
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
        verbose_name = _('Lugar Almacenamiento')
        verbose_name_plural = _('Lugares de Almacenamiento')
        permissions = permissions_storage

    nombre = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _('Nombre')
    )
    descripcion = models.TextField(
            max_length = 1000,
            default = '',
            verbose_name = _("Descripción")
    )

    capacidad = models.IntegerField(
            verbose_name = _("Capacidad")
    )
    temperatura = models.DecimalField(
            max_digits = 5,
            decimal_places = 2,
            verbose_name = _("Temperatura")
    )
    estado = models.CharField(
            max_length = 100,
            default = '',
            verbose_name = _('Estado'),
            null = True
    )
    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )

    #id= models.CharField(
    #        max_length = 100,
    #        default = '',
    #        verbose_name = _("Identificación"),
    #        null = False,
    #        primary_key = True
    #)
    
    def __unicode__(self):
        return self.id+":"+self.nombre




class LugarAlmacenamientoEnLab(models.Model):
    """Relación entre :class:`LugarAlmacenamiento` y :class:`LaboratorioProfile`
        Se encarga de:
            * Definir la posición del lugar Almacenamiento en donde esta guardada
            * Permite guardar en la base de datos esta relación

        Atributos:
            :idLaboratorio (String): Id del laboratorio.
            :idLugar (String): Id del lugar Almacenamiento
            :posX (Integer): Posición x en la que el lugar Almacenamiento esta guardado.
            :posY (Integer): Posición y en la que el lugar Almacenamiento esta guardado.
     """

    class Meta:
        verbose_name = "Lugar de almacenamiento en Laboratorio"
        verbose_name_plural = 'Lugares de almacenamiento en Laboratorio'

    idLaboratorio = models.ForeignKey(
            LaboratorioProfile,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Laboratorio")
    )
    idLugar = models.OneToOneField(
            LugarAlmacenamiento,
            blank = False,
            null = False,
            on_delete = models.CASCADE,
            verbose_name = _("Lugar Almacenamiento"),
            primary_key = True
    )
    posX = models.PositiveIntegerField(
            verbose_name = _("Posición X")
    )
    posY = models.PositiveIntegerField(
            verbose_name = _("Posición Y")
    )

    def __unicode__(self):
        return self.idLaboratorio.id + ":" + str(self.posX) + "," + str(self.posY)


class Protocolo(models.Model):
    """Representación de Protocolos
         Se encarga de:
             * Definir las caracteristicas de un protocolo
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre del protocolo.
             :descripción (String): descripción del protocolo
             :objetivo (String): Objetivo del protocolo
        Permisos:
            :can_addProtocol: Permite agregar protocolo
            :can_editProtocol: Permite modificar protocolo
            :can_viewProtocol: Permite ver protocolo
      """

    class Meta:
        verbose_name = _('Protocolo')
        verbose_name_plural = _('Protocolos')
        permissions = permissions_protocol

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Nombre Protocolo")
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción del Protocolo")
    )
    objetivo = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Objetivo del Protocolo")
    )


class Paso(models.Model):
    """Representación de Paso
         Se encarga de:
             * Definir las caracteristicas de un paso
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre del paso.
             :descripción (String): descripción del paso
             :protocolo (Relacion): Seleccion de Protocolo
        Permisos:
            :can_addStep: Permite agregar paso
            :can_editStep: Permite modificar paso
            :can_viewStep: Permite ver paso
      """

    class Meta:
        verbose_name = _('Paso')
        verbose_name_plural = _('Pasos')
        permissions = permissions_step

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = "Nombre paso"
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = "descripción del paso"
    )
    protocolo = models.ForeignKey(
            Protocolo,
            blank = False,
            null = True,
            verbose_name = "Seleccion de Protocolo"
    )


class Muestra(models.Model):
    """Representación de Muestra
         Se encarga de:
             * Definir las caracteristicas de un muestra
             * Permite guardar en la base de datos esta entidad

         Atributos:
             :nombre (String): Nombre de la muestra
             :descripción (String): descripción de la muestra
             :valor (Numeric): Valor por unidad
             :activa (Boolean): Estado de disponibilidad de la muestra
             :controlado (Boolean): Estado de restriccion de la muestra
             :imagen (Image): Imagen de la muestra
             :unidadBase (String): Unidad de medida de la muestra
        Permisos:
            :can_addSample: Permite agregar muestra
            :can_editSample: Permite modificar muestra
            :can_viewSample: Permite ver muestra
      """

    class Meta:
        verbose_name = _('Muestra')
        verbose_name_plural = _('Muestras')
        permissions = permissions_sample

    nombre = models.CharField(
            max_length = 1000,
            blank = False,
            null = True,
            verbose_name = _("Nombre de la Muestra")
    )
    descripcion = models.TextField(
            max_length = 1000,
            blank = False,
            null = True,
            verbose_name = _("Descripción de la Muestra")
    )

    valor = models.DecimalField(
            max_digits = 5,
            decimal_places = 2,
            null = True,
            verbose_name = _("Valor")
    )
    activa = models.BooleanField(
            default = True,
            verbose_name = _("Activa")
    )
    controlado = models.BooleanField(
            blank = False,
            default = False,
            verbose_name = _("Muestra Controlada")
    )

    imagen = models.ImageField(
            upload_to = 'images',
            verbose_name = _("Imagen"),
            default = 'images/image-not-found.jpg'
    )
    unidadBase = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Unidad de Medida")
    )

    def __unicode__(self):
        return 'Muestra: ' + self.nombre

    def calc_disp(self):
        bandejas = Bandeja.objects.filter(muestra = self)
        for bandeja in bandejas:
            if not bandeja.libre:
                return 'Si'
        return 'No'

    def calc_cuantos_disp(self):
        contador = 0
        bandejas = Bandeja.objects.filter(muestra = self)
        for bandeja in bandejas:
            if not bandeja.libre:
                contador += 1
        return contador

    def calc_controled(self):
        if self.controlado:
            return 'Si'
        else:
            return 'No'

    def calc_posicion(self):
        '''
        Retorna -1 cuando la muestra no esta activa o no se encuentra en ningun lugar de almacenimiento
        '''
        bandeja = Bandeja.objects.filter(muestra=self).first()
        if bandeja is not None:
           lugar = bandeja.lugarAlmacenamiento
           laboratorio = LugarAlmacenamientoEnLab.objects.filter(idLugar=lugar).first().idLaboratorio
           return laboratorio.__unicode__()
        return "No disponible"

class Bandeja(models.Model):
    """Representación de una bandeja del lugar de almacenamiento.
        Se encarga de:
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos la bandeja del lugar de almacenamiento

        Atributos:

            :libre (Decimal): Indica si esta libre la bandeja del lugar de almacenamiento.
            :muestra (String): Relación con la entidad muestra.
            :lugarAlmacenamiento (Decimal): Relación con la entidad lugar de almacenamiento.
    """

    class Meta:
        verbose_name = _('Bandeja')
        verbose_name_plural = _('Bandejas')
        permissions = permissions_tray

    libre = models.BooleanField(
            blank = False,
            default = True,
            verbose_name = _("Libre")
    )
    muestra = models.ForeignKey(
            Muestra,
            blank = False,
            null = True,
            verbose_name = _("Selección de Muestra")
    )
    posicion = models.IntegerField(
        null=True,
        verbose_name="Posicion"
    )
    lugarAlmacenamiento = models.ForeignKey(
            LugarAlmacenamiento,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Selección de Lugar Almacenamiento")
    )

    posicion= models.PositiveIntegerField(
            verbose_name = _("Número de bandeja"),
            null=False,
            default=1,
            blank=False
    )

    def __unicode__(self):
        return 'Bandeja: ' + self.lugarAlmacenamiento.__unicode__()+ " "+ str(self.posicion)







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
        verbose_name = _('Solicitud')
        verbose_name_plural = _('Solicitudes')
        permissions = permissions_request

    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción de la Solicitud")
    )
    fechaInicial = models.DateTimeField(
            blank = False,
            null = True,
            verbose_name = _("Fecha Inicial"),
            default = timezone.now

    )
    fechaFinal = models.DateTimeField(
            blank = False,
            null = True,
            verbose_name = _("Fecha Final"),
            default = timezone.now
    )
    estado = models.CharField(
            max_length = 30,
            blank = False,
            null = True,
            verbose_name = _("Estado Solicitud")
    )
    solicitante = models.ForeignKey(
            Usuario,
            blank = False,
            null = True,
            verbose_name = _("Solicitante"),
            related_name = "solicitudesHechas"
    )
    aprobador = models.ForeignKey(
            Usuario,
            blank = False,
            null = True,
            verbose_name = _("Aprobador"),
            related_name = "solicitudesAprobadas"
    )
    fechaActual = models.DateField(
            blank = False,
            null = True,
            verbose_name = _("Fecha Actual"),
            default = timezone.now
    )
    paso = models.ForeignKey(
            Paso,
            blank = False,
            null = True,
            verbose_name = _("Selección de Paso")
    )


    def __unicode__(self):
        return self.solicitante.__unicode__()+" "+self.estado




class MuestraSolicitud(models.Model):
    """Relación entre :class:`Muestra` y :class:`Solicitud` Detalle de solicitud
        Se encarga de:
            * Definir la relacion entre solicitud y muestras solicitadas
            * Permite guardar en la base de datos el detalle de una solicitud

        Atributos:
            :solicitud (Decimal): Id solicitud.
            :muestra (Decimal): Selección de Muestra
            :cantidad (Integer): Cantidad de muestra.
            :tipo (String):Tipo solicitud.
        Permisos:
            :can_solMuestra: Permite solicitar muestra
         """

    class Meta:
        verbose_name = _('Solicitud de Muestra')
        verbose_name_plural = _('Solicitudes de Muestra')

    solicitud = models.OneToOneField(Solicitud)
    muestra = models.ForeignKey(
            Muestra,
            blank = False,
            null = True,
            verbose_name = _("Selección de Muestra")
    )
    cantidad = models.IntegerField(
            blank = False,
            null = True,
            default = 1,
            verbose_name = _("Cantidad de Muestra")
    )
    tipo = models.CharField(
            max_length = 30,
            blank = False,
            null = True,
            verbose_name = _("Tipo Solicitud")
    )


class MaquinaSolicitud(models.Model):
    class Meta:
        verbose_name = _('Solicitud de Máquina')
        verbose_name_plural = _('Solicitudes de Máquina')

    solicitud = models.OneToOneField(Solicitud)
    maquina = models.ForeignKey(
            MaquinaProfile,
            blank = False,
            null = True,
            verbose_name = _("Selección de Máquina")
    )
    def __unicode__(self):
        return self.maquina.__unicode__()+" "+self.solicitud.__unicode__()

    def as_json(self,id_user):
        return dict(id_maquina=self.maquina.idSistema,id=self.solicitud.id,encargado=self.solicitud.solicitante.nombre_completo(),
            start=self.solicitud.fechaInicial.isoformat().replace('+00:00','-05:00'),end=self.solicitud.fechaFinal.isoformat().replace('+00:00','-05:00'),
            className='envent',editable=True if id_user==self.solicitud.solicitante.user.id else False,overlap=False,paso=self.solicitud.paso.nombre)


class Proyecto(models.Model):
    """Representación de un proyecto.
        Se encarga de:
            * Definir las caracteristicas de un proyecto
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos esta entidad

        Atributos:
            :nombre (String): Nombre proyecto
            :descripción (String): descripción del proyecto.
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
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')
        permissions = permissions_project

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Nombre del Proyecto")
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción del Proyecto")
    )
    objetivo = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Objetivo del Proyecto")
    )
    lider = models.ForeignKey(
            Usuario,
            blank = False,
            null = True,
            verbose_name = _("Líder"),
            related_name = "lider"
    )
    asistentes = models.ManyToManyField(
            Usuario,
            verbose_name = _("Asistentes"),
            related_name = "asistentes"
    )
    activo = models.BooleanField(
            blank = False,
            null = False,
            default = True,
            verbose_name = _('Estado de Actividad del Proyecto')
    )


class Experimento(models.Model):
    """Representación de un experimento.
        Se encarga de:
            * Definir las caracteristicas de un experimento
            * Definir las restricciónes basicas de los campos
            * Permite guardar en la base de datos esta entidad

        Atributos:
            :nombre (String): Nombre expermento
            :descripción (String): descripción del experimento.
            :objetivo (String): Objetivo del experimento
            :projecto (Decimal): Seleccion de Proyecto
            :protocolos (Object): Lista de protocolos
        Permisos:
            :can_addExperiment: Permite agregar experimento
            :can_editExperiment: Permite modificar experimento
            :can_viewExperiment: Permite ver experimento
    """

    class Meta:
        verbose_name = _('Experimento')
        verbose_name_plural = _('Experimentos')
        permissions = permissions_experiment

    nombre = models.CharField(
            max_length = 50,
            blank = False,
            null = True,
            verbose_name = _("Nombre Expermento")
    )
    descripcion = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Descripción del Experimento")
    )
    objetivo = models.TextField(
            max_length = 200,
            blank = False,
            null = True,
            verbose_name = _("Objetivo del Experimento")
    )
    projecto = models.ForeignKey(
            Proyecto,
            blank = False,
            null = True,
            on_delete = models.CASCADE,
            verbose_name = _("Proyecto"),
            related_name = "proyecto"
    )
    protocolos = models.ManyToManyField(
            Protocolo,
            related_name = "experimento"
    )
