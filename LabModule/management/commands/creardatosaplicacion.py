# -*- coding: utf-8 -*-
import json
import urllib2
from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.templatetags.static import static

from LabModule.models import Bandeja
from LabModule.models import Experimento
from LabModule.models import LaboratorioProfile
from LabModule.models import LugarAlmacenamiento
from LabModule.models import LugarAlmacenamientoEnLab
from LabModule.models import MaquinaEnLab
from LabModule.models import MaquinaProfile
from LabModule.models import Muestra
from LabModule.models import Paso
from LabModule.models import Protocolo
from LabModule.models import Proyecto
from LabModule.models import TipoDocumento
from LabModule.models import Usuario

SUPERUSUARIO = getattr(settings, "SUPERUSUARIO", 'admin')
CONTRASENA = getattr(settings, "CONTRASENA", '1a2d3m4i5n6')
EMAIL_HOST_USER = getattr(settings, "EMAIL_HOST_USER", 'admin@admin.com')

can_addProject = Permission.objects.get(name = 'proyecto||agregar')
can_editProject = Permission.objects.get(name = 'proyecto||editar')
can_listProject = Permission.objects.get(name = 'proyecto||listar')
can_viewProject = Permission.objects.get(name = 'proyecto||ver')
can_addExperiment = Permission.objects.get(name = 'experimento||agregar')
can_editExperiment = Permission.objects.get(name = 'experimento||editar')
can_listExperiment = Permission.objects.get(name = 'experimento||listar')
can_viewExperiment = Permission.objects.get(name = 'experimento||ver')
can_addUser = Permission.objects.get(name = 'usuario||agregar')
can_editUser = Permission.objects.get(name = 'usuario||editar')
can_listUser = Permission.objects.get(name = 'usuario||listar')
can_viewUser = Permission.objects.get(name = 'usuario||ver')
can_addLab = Permission.objects.get(name = 'laboratorio||agregar')
can_editLab = Permission.objects.get(name = 'laboratorio||editar')
can_listLab = Permission.objects.get(name = 'laboratorio||listar')
can_viewLab = Permission.objects.get(name = 'laboratorio||ver')
can_addMachine = Permission.objects.get(name = 'maquina||agregar')
can_editMachine = Permission.objects.get(name = 'maquina||editar')
can_listMachine = Permission.objects.get(name = 'maquina||listar')
can_viewMachine = Permission.objects.get(name = 'maquina||ver')
can_requestMachine = Permission.objects.get(name = 'maquina||solicitar')
can_addStorage = Permission.objects.get(name = 'almacenamiento||agregar')
can_editStorage = Permission.objects.get(name = 'almacenamiento||editar')
can_listStorage = Permission.objects.get(name = 'almacenamiento||listar')
can_viewStorage = Permission.objects.get(name = 'almacenamiento||ver')
can_requestStorage = Permission.objects.get(name = 'almacenamiento||solicitar')
can_addProtocol = Permission.objects.get(name = 'protocolo||agregar')
can_editProtocol = Permission.objects.get(name = 'protocolo||editar')
can_listProtocol = Permission.objects.get(name = 'protocolo||listar')
can_viewProtocol = Permission.objects.get(name = 'protocolo||ver')
can_addStep = Permission.objects.get(name = 'paso||agregar')
can_editStep = Permission.objects.get(name = 'paso||editar')
can_listStep = Permission.objects.get(name = 'paso||listar')
can_viewStep = Permission.objects.get(name = 'paso||ver')
can_addSample = Permission.objects.get(name = 'muestra||agregar')
can_editSample = Permission.objects.get(name = 'muestra||editar')
can_listSample = Permission.objects.get(name = 'muestra||listar')
can_viewSample = Permission.objects.get(name = 'muestra||ver')
can_requestSample = Permission.objects.get(name = 'muestra||solicitar')
can_listRequest = Permission.objects.get(name = 'solicitud||listar')
can_viewRequest = Permission.objects.get(name = 'solicitud||ver')
can_manageRequest = Permission.objects.get(name = 'solicitud||admin')
can_addTray = Permission.objects.get(name = 'bandeja||agregar')
can_editTray = Permission.objects.get(name = 'bandeja||editar')
can_listTray = Permission.objects.get(name = 'bandeja||listar')
can_viewTray = Permission.objects.get(name = 'bandeja||ver')


def crearTiposDocumento():
    print ('Creando Tipos de Documento'),
    nuevoTipoDoc, tipoDocExistente = TipoDocumento.objects.get_or_create(nombre_corto = 'CC')
    if tipoDocExistente:
        nuevoTipoDoc.descripcion = 'Cedula de Ciudadania'
        nuevoTipoDoc.save()
        print ('.'),
        return 0
    print ('...'),
    return 1


def crearLaboratorio():
    print ('Creando Laboratorios'),
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio principal",
                                                                            id = "LAB001")
    print ('.'),
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio Secundario",
                                                                            id = "LAB002")
    print ('.'),
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio Terciario",
                                                                            id = "LAB003")
    print ('.'),
    if laboratioExistente:
        return 0
    print ('...'),
    return 1


def crearMaquina():
    print ('Creando Maquinas'),
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio principal",
                                                                            id = "LAB001")
    rta = 1
    with open(".///" + static('lab_static/json/maquinas.json')) as data_file:
        data = json.load(data_file)
        for maquina in data:
            nuevaMaquina, maquinaExistente = MaquinaProfile.objects.get_or_create(nombre = maquina['nombre'],
                                                                                  descripcion = maquina['descripcion'],
                                                                                  idSistema = maquina['idSistema'],
                                                                                  con_reserva = maquina['con_reserva']
                                                                                  )
            if maquinaExistente:
                if not maquina['imagen'] == '':
                    img_url = maquina['imagen']
                    img_filename = urlparse(img_url).path.split('/')[-1]
                    img_temp = NamedTemporaryFile()
                    img_temp.write(urllib2.urlopen(img_url).read())
                    img_temp.flush()
                    nuevaMaquina.imagen.save(img_filename, File(img_temp))

            nuevare, exre = MaquinaEnLab.objects.get_or_create(idLaboratorio = nuevoLab,
                                                               idMaquina = nuevaMaquina,
                                                               posX = maquina['x'],
                                                               posY = maquina['y'])
            print ('.'),
            if maquinaExistente:
                rta = 0
    return rta


def crearBandeja():
    print('Creando Bandejas'),
    print ('.'),
    return 0


def crearAlmacenamiento():
    rta = 1
    print('Creando Lugares de Almacenamiento'),
    with open(".///" + static('lab_static/json/lugares.json')) as data_file:
        data = json.load(data_file)
        idAct = 0

        for row in data:
            nombre = row['nombre']
            descripcion = row['descripcion']
            capacidad = row['capacidad']
            temperatura = row['temperatura']
            estado = row['estado']
            imagen = row['imagen']
            cantidad = row['cantidad']
            posX = row['posX']
            posY = row['posY']
            idLaboratorio = row['idLaboratorio']
            nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(id = idLaboratorio)
            img_url = imagen
            img_filename = urlparse(img_url).path.split('/')[-1]
            img_temp = NamedTemporaryFile()
            img_temp.write(urllib2.urlopen(img_url).read())
            img_temp.flush()
            for i in range(1, int(cantidad) + 1):
                idAct += 1
                nuevoLugar, lugarCreado = LugarAlmacenamiento.objects.get_or_create(nombre = nombre + " " + str(i),
                                                                                    descripcion = descripcion,
                                                                                    capacidad = capacidad,
                                                                                    temperatura = temperatura,
                                                                                    estado = estado,
                                                                                    id = idAct)
                nuevoLugar.imagen.save(img_filename, File(img_temp))
                print ('.'),
                if lugarCreado:
                    rta = 0
                    xPos = int(posX) + (i - 1)
                    yPos = int(posY)
                    if xPos > 10:
                        xPos = xPos - 10
                        yPos = yPos + 1
                    nuevloLugarEnLab, lugarENLabExistente = LugarAlmacenamientoEnLab.objects.get_or_create(
                            idLaboratorio = nuevoLab, idLugar = nuevoLugar, posX = xPos, posY = yPos)
    return rta


def crearMuestra():
    rta = 1
    print ('Creando Muestras'),
    with open(".///" + static('lab_static/json/muestras.json')) as data_file:
        data = json.load(data_file)
        idAct = 0
        for row in data:
            nombre = row['nombre']
            descripcion = row['descripcion']
            Tipo = row['Tipo']
            valor = row['valor']
            activa = row['activa']
            controlado = row['controlado']
            imagen = row['imagen']
            unidadBase = row['unidadBase']
            idAlmacenamiento = row['idAlmacenamiento']
            nuevaMuestra, mustraCreada = Muestra.objects.get_or_create(nombre = nombre, descripcion = descripcion,
                                                                       valor = valor, activa = activa,
                                                                       controlado = controlado,
                                                                       unidadBase = unidadBase)
            nuevoLugar, LugarExistente = LugarAlmacenamiento.objects.get_or_create(id = idAlmacenamiento)
            if mustraCreada:
                print ('.'),
                rta = 0
                img_url = imagen
                img_filename = urlparse(img_url).path.split('/')[-1]
                img_temp = NamedTemporaryFile()
                img_temp.write(urllib2.urlopen(img_url).read())
                img_temp.flush()
                nuevaMuestra.imagen.save(img_filename, File(img_temp))
                cuenta = Bandeja.objects.filter(lugarAlmacenamiento = nuevoLugar).count()
                posicion = 1 if cuenta == 0 else cuenta + 1
                nuevaBandeja, bandejaExistenet = Bandeja.objects.get_or_create(muestra = nuevaMuestra,
                                                                               lugarAlmacenamiento = nuevoLugar,
                                                                               posicion = posicion,
                                                                               libre = False)

    return rta


def crearProyecto():
    print ('Crear Proyectos'),
    nuevoProyecto, noexistia = Proyecto.objects.get_or_create(nombre = "Colombia Viva")

    nuevoProyecto.descripcion = "Proyecto para sintetizar una droga que reduzca el cansancio"
    nuevoProyecto.objetivo = "Crear NZT"
    nuevoProyecto.lider = Usuario.objects.get(nombre_usuario = 'acastro')
    asistentes = Usuario.objects.all().filter(nombre_usuario__startswith = 'mgalindo')
    asistentes = list(asistentes)
    nuevoProyecto.asistentes.add(*asistentes)
    nuevoProyecto.activo = True
    print ('.'),
    return 0


def crearExperimento():
    print('Crear Experimento'),
    print ('.'),
    nuevoExperimento, noexistiaexp = Experimento.objects.get_or_create(nombre = "Experimento Colombia Viva")
    nuevoExperimento.descripcion = "Experimento que hace parte de Colombia Viva"
    nuevoExperimento.objetivo = "Crear"
    protocolos = Protocolo.objects.all()
    protocolos = list(protocolos)
    nuevoExperimento.protocolos.add(*protocolos)
    nuevoExperimento.projecto = Proyecto.objects.get(nombre = "Colombia Viva")
    nuevoExperimento.save()
    return 0


def crearProtocolo():
    print('Crear Protocolos'),
    print ('.'),
    nuevoProtocolo, noexistiaproto = Protocolo.objects.get_or_create(nombre = "Protocolo Colombia Viva")
    nuevoProtocolo.descripcion = "Protocolo que hace parte de Colombia Viva"
    nuevoProtocolo.objetivo = "Crear"
    nuevoProtocolo.save()
    return 0


def crearPaso():
    print ('Crear Pasos'),
    print ('.'),
    nuevoPaso, noexistiapaso = Paso.objects.get_or_create(nombre = "Paso Colombia Viva")
    nuevoPaso.descripcion = "Paso que hace parte de Colombia Viva"
    nuevoPaso.objetivo = "Crear"
    protocolo = Protocolo.objects.get(nombre = 'Protocolo Colombia Viva')
    nuevoPaso.protocolo = protocolo
    nuevoPaso.save()
    return 0


def createGroups():
    print('Crear Grupos'),
    cientificos, created1 = Group.objects.get_or_create(name = 'Cientifico Experimentado')
    print ('.'),
    asistentes, created2 = Group.objects.get_or_create(name = 'Asistente de Laboratorio')
    print ('.'),
    jefes, created3 = Group.objects.get_or_create(name = 'Jefe de Laboratorio')
    print ('.'),

    maquinasVer = Permission.objects.get(name = 'maquina||ver')
    maquinasSolicitar = Permission.objects.get(name = 'maquina||solicitar')
    agregarUsuario = Permission.objects.get(name = 'usuario||agregar')
    listarmuestras = Permission.objects.get(name = 'muestra||listar')
    muestraVer = Permission.objects.get(name = 'muestra||ver')
    muestraSolicitar = Permission.objects.get(name = 'muestra||solicitar')

    cientificos.permissions.add(
            can_addProject,
            can_editProject,
            can_listProject,
            can_viewProject,
            can_addExperiment,
            can_editExperiment,
            can_listExperiment,
            can_viewExperiment,
            can_addUser,
            can_editUser,
            can_listUser,
            can_viewUser,
            can_addLab,
            can_editLab,
            can_listLab,
            can_viewLab,
            can_addMachine,
            can_editMachine,
            can_listMachine,
            can_viewMachine,
            can_addStorage,
            can_editStorage,
            can_listStorage,
            can_viewStorage,
            can_addProtocol,
            can_editProtocol,
            can_listProtocol,
            can_viewProtocol,
            can_addStep,
            can_editStep,
            can_listStep,
            can_viewStep,
            can_addSample,
            can_editSample,
            can_listSample,
            can_viewSample,
            can_listRequest,
            can_viewRequest,
            can_addTray,
            can_editTray,
            can_listTray,
            can_viewTray,
    )
    jefes.permissions.add(
            can_listRequest,
            can_viewRequest,
            can_manageRequest,
            can_listMachine,
            can_viewMachine,
            can_editMachine,
            can_listStorage,
            can_viewStorage,
            can_editStorage,
            can_addSample,
            can_editSample,
            can_listSample,
            can_viewSample,
            can_addUser,
    )
    asistentes.permissions.add(
            can_listMachine,
            can_viewMachine,
            can_requestMachine,
            can_listSample,
            can_viewSample,
            can_requestSample,
            can_listRequest,
    )
    if created1 or created2 or created3:
        return 0
    return 1


def crearAsistente(user, num, tipDocumento, asistentes):
    print ('Crear Asistentes'),
    exist_asistente, new_asistente = User.objects.get_or_create(
            username = user + str(num))
    print ('...'),
    if new_asistente:
        exist_asistente.email = user + str(num) + '@uniandes.edu.co'
        exist_asistente.set_password(CONTRASENA)
        exist_asistente.groups.add(asistentes)
        exist_asistente.save()

        exist_usuario, new_usuario = Usuario.objects.get_or_create(
                nombre_usuario = user + str(num),
                correo_electronico = user + str(num) + '@uniandes.edu.co',
                codigo_usuario = '19950914' + str(num),
                nombres = 'Monica',
                apellidos = 'Galindo',
                telefono = '7453698',
                userNatIdTyp = tipDocumento,
                userNatIdNum = '31852496',
                grupo = asistentes,
                user = exist_asistente,
                contrasena = CONTRASENA,
        )
    print ('Asistentes Creadas')


def createUsers():
    print ('Crear Usuarios'),
    cientificos = Group.objects.get(name = 'Cientifico Experimentado')
    jefes = Group.objects.get(name = 'Jefe de Laboratorio')
    asistentes = Group.objects.get(name = 'Asistente de Laboratorio')

    tipDocumento = TipoDocumento.objects.get(nombre_corto = 'CC')

    exist_cientifico, new_cientifico = User.objects.get_or_create(username = 'acastro')

    if new_cientifico:
        exist_cientifico.email = 'acastro@uniandes.edu.co'
        exist_cientifico.set_password(CONTRASENA)
        exist_cientifico.groups.add(cientificos)
        exist_cientifico.save()


    exist_usuario, new_usuario = Usuario.objects.get_or_create(
            nombre_usuario = 'acastro',
            correo_electronico = 'acastro@uniandes.edu.co',
            codigo_usuario = '19950912',
            nombres = 'Aquiles',
            apellidos = 'Castro',
            telefono = '7453694',
            userNatIdTyp = tipDocumento,
            userNatIdNum = '79325416',
            grupo = cientificos,
            user = exist_cientifico,
            contrasena = CONTRASENA,
    )
    print ('.'),
    exist_jefe, new_jefe = User.objects.get_or_create(username = 'bcamelas')
    if new_jefe:
        exist_jefe.email = 'bcamelas@uniandes.edu.co'
        exist_jefe.set_password(CONTRASENA)
        exist_jefe.groups.add(jefes)
        exist_jefe.save()


    exist_usuario, new_usuario = Usuario.objects.get_or_create(
            nombre_usuario = 'bcamelas',
            correo_electronico = 'bcamelas@uniandes.edu.co',
            codigo_usuario = '19950913',
            nombres = 'Benito',
            apellidos = 'Camelas',
            telefono = '7453619',
            userNatIdTyp = tipDocumento,
            userNatIdNum = '79163482',
            grupo = jefes,
            user = exist_jefe,
            contrasena = CONTRASENA,
    )
    print ('.')
    for i in range(10):
        crearAsistente('mgalindo', i, tipDocumento, asistentes)

    exist_admin = User.objects.get(username = SUPERUSUARIO)
    exist_usuario, new_usuario = Usuario.objects.get_or_create(
            nombre_usuario = SUPERUSUARIO,
            correo_electronico = EMAIL_HOST_USER,
            codigo_usuario = '100000',
            nombres = 'Administrador',
            apellidos = 'Administrador',
            telefono = '100000',
            userNatIdTyp = tipDocumento,
            userNatIdNum = '1000000',
            grupo = cientificos,
            user = exist_admin,
            contrasena = CONTRASENA,
    )
    if new_cientifico or new_jefe:
        return 0
    return 1


class Command(BaseCommand):
    help = 'Esto crea un set de datos básico'

    def handle(self, *args, **options):

        def execute_function(self, function_name, result_text, *args, **options):

            if globals()[function_name]() == 0:
                self.stdout.write(self.style.SUCCESS('"%sCreados."' % result_text))
            else:
                self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % result_text))

        lista_instalacion = [['crearTiposDocumento', 'Tipos de Documentos '],
                             ['crearLaboratorio', 'Laboratorios '],
                             ['crearMaquina', 'Maquinas '],
                             ['createGroups', 'Grupos '],
                             ['createUsers', 'Usuarios '],
                             ['crearBandeja', 'Bandejas '],
                             ['crearAlmacenamiento', 'Almacenamientos '],
                             ['crearMuestra', 'Muestras '],
                             ['crearProyecto', 'Proyectos '],
                             ['crearProtocolo', 'Protocolos '],
                             ['crearExperimento', 'Experimentos '],
                             ['crearPaso', 'Pasos '],
                             ]

        for functions in lista_instalacion:
            execute_function(self, function_name = functions[0], result_text = functions[1])
