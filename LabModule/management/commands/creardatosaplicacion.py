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

from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.Experimento import Experimento
from LabModule.app_models.Laboratorio import Laboratorio
from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.Mueble import Mueble
from LabModule.app_models.MuebleEnLab import MuebleEnLab
from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.MuestraEnBandeja import MuestraEnBandeja
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Protocolo import Protocolo
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.TipoDocumento import TipoDocumento
from LabModule.app_models.Usuario import Usuario

SUPERUSUARIO = getattr(settings, 'SUPERUSUARIO', 'admin')
CONTRASENA = getattr(settings, 'CONTRASENA', '1a2d3m4i5n6')
EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', 'admin@admin.com')

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


def print_status_message(status):
    if status:
        print ('.'),
    else:
        print ('...'),


def crear_tipos_documento():
    doc_type_history = False
    print ('Creando Tipos de Documento'),
    new_doc_type, doc_type_is_created = TipoDocumento.objects.get_or_create(nombre_corto = 'CC',
                                                                            descripcion = 'Cédula de Ciudadanía')
    print_status_message(status = doc_type_is_created)
    doc_type_history = doc_type_history | doc_type_is_created
    new_doc_type.save()

    if doc_type_history:
        return 0
    return 1


def crear_laboratorios():
    lab_history = False
    print ('Creando Laboratorios'),
    new_lab, lab_is_created = Laboratorio.objects.get_or_create(nombre = 'Laboratorio Principal',
                                                                idLaboratorio = 'LAB001',
                                                                numX = 20,
                                                                numY = 20)
    print_status_message(status = lab_is_created)
    lab_history = lab_history | lab_is_created
    new_lab.save()
    new_lab, lab_is_created = Laboratorio.objects.get_or_create(nombre = 'Laboratorio Secundario',
                                                                idLaboratorio = 'LAB002',
                                                                numX = 20,
                                                                numY = 20)
    print_status_message(status = lab_is_created)
    lab_history = lab_history | lab_is_created
    new_lab.save()
    new_lab, lab_is_created = Laboratorio.objects.get_or_create(nombre = 'Laboratorio Terciario',
                                                                idLaboratorio = 'LAB003',
                                                                numX = 20,
                                                                numY = 20)
    print_status_message(status = lab_is_created)
    lab_history = lab_history | lab_is_created
    new_lab.save()
    if lab_history:
        return 0
    return 1


def crear_maquinas():
    machine_history = False
    print ('Creando Maquinas'),
    new_lab, lab_is_created = Laboratorio.objects.get_or_create(nombre = 'Laboratorio Principal',
                                                                idLaboratorio = 'LAB001',
                                                                numX = 20,
                                                                numY = 20)
    print_status_message(status = lab_is_created)
    machine_history = machine_history | lab_is_created
    new_lab.save()
    with open('.///' + static('lab_static/json/maquinas.json')) as data_file:
        data = json.load(data_file)
        for machine in data:
            new_mueble, mueble_is_created = Mueble.objects.get_or_create(nombre = machine['nombre'],
                                                                         descripcion = machine['descripcion'],
                                                                         tipo = 'maquina'
                                                                         )

            print_status_message(status = mueble_is_created)
            machine_history = machine_history | mueble_is_created
            new_mueble.save()

            if mueble_is_created:
                new_machine, machine_is_created = Maquina.objects.get_or_create(mueble = new_mueble,
                                                                                con_reserva = machine['con_reserva'],
                                                                                idSistema = machine['idSistema'])
                print_status_message(status = machine_is_created)
                machine_history = machine_history | machine_is_created
                new_machine.save()
                if not machine['imagen'] == '':
                    img_url = machine['imagen']
                    img_filename = urlparse(img_url).path.split('/')[-1]
                    img_temp = NamedTemporaryFile()
                    img_temp.write(urllib2.urlopen(img_url).read())
                    img_temp.flush()
                    new_mueble.imagen.save(img_filename, File(img_temp))

            new_machine_loc, machine_loc_is_created = MuebleEnLab.objects.get_or_create(idLaboratorio = new_lab,
                                                                                        idMueble = new_mueble,
                                                                                        posX = machine['x'],
                                                                                        posY = machine['y'])
            print_status_message(status = machine_loc_is_created)
            machine_history = machine_history | machine_loc_is_created
            new_machine_loc.save()
    if machine_history:
        return 0
    return 1


def crear_bandeja():
    print('Creando Bandejas'),
    print ('.'),
    return 0


def crear_almacenamientos():
    storage_history = False
    print('Creando Lugares de Almacenamiento'),

    with open('.///' + static('lab_static/json/lugares.json')) as data_file:
        data = json.load(data_file)
        id_storage = 0
        for row in data:
            nombre = row['nombre']
            descripcion = row['descripcion']
            capacidad = row['capacidad']
            temperatura = row['temperatura']
            estado = row['estado']
            imagen = row['imagen']
            cantidad = row['cantidad']
            pos_x = row['posX']
            pos_y = row['posY']
            id_laboratorio = row['idLaboratorio']
            new_lab, lab_is_created = Laboratorio.objects.get_or_create(idLaboratorio = id_laboratorio)
            print_status_message(status = lab_is_created)
            storage_history = storage_history | lab_is_created
            new_lab.save()
            created = False
            for i in range(1, int(cantidad) + 1):
                id_storage += 1
                new_mueble, mueble_is_created = Mueble.objects.get_or_create(nombre = nombre + ' ' + str(i),
                                                                             descripcion = descripcion,
                                                                             estado = estado,
                                                                             tipo = 'almacenamiento'
                                                                             )
                print_status_message(status = mueble_is_created)
                storage_history = storage_history | mueble_is_created
                new_mueble.save()
                
                new_storage, storage_is_created = Almacenamiento.objects.get_or_create(mueble = new_mueble,
                                                                                           temperatura = temperatura,
                                                                                           numZ = capacidad,idSistema = id_storage,numY=2,numX=5)
                if storage_is_created:        
                    print_status_message(status = storage_is_created)
                    storage_history = storage_history | storage_is_created
                    new_storage.save()
                    
                    for i in range(1,capacidad+1):
                        nueva_bandeja,bandeja_creada=Bandeja.objects.get_or_create(almacenamiento=new_storage,posicion=i)

                    if not created:
                        img_url = imagen
                        img_filename = urlparse(img_url).path.split('/')[-1]
                        img_temp = NamedTemporaryFile()
                        img_temp.write(urllib2.urlopen(img_url).read())
                        img_temp.flush()
                        new_mueble.imagen.save(img_filename, File(img_temp))
                        created = True
                    if storage_is_created:
                        x_pos = int(pos_x) + (i - 1)
                        y_pos = int(pos_y)
                        if x_pos > 10:
                            x_pos = x_pos - 10
                            y_pos = y_pos + 1

                        new_storage_loc, storage_loc_is_created = MuebleEnLab.objects.get_or_create(
                                idLaboratorio = new_lab,
                                idMueble = new_mueble,
                                posX = x_pos,
                                posY = y_pos)
                        print_status_message(status = storage_loc_is_created)
                        storage_history = storage_history | storage_loc_is_created
                        new_storage_loc.save()
    if storage_history:
        return 0
    return 1


def crear_muestras():
    sample_history = False
    print ('Creando Muestras'),
    with open('.///' + static('lab_static/json/muestras.json')) as data_file:
        data = json.load(data_file)

        for row in data:
            nombre = row['nombre']
            descripcion = row['descripcion']
            valor = row['valor']
            activa = row['activa']
            controlado = row['controlado']
            imagen = row['imagen']
            unidad_base = row['unidadBase']
            id_almacenamiento = row['idAlmacenamiento']
            posicion=row['posicion']
            alamcenamientosPosibles = row['alamcenamientosPosibles']
            new_sample, sample_is_created = Muestra.objects.get_or_create(nombre = nombre,
                                                                          descripcion = descripcion,
                                                                          valor = valor,
                                                                          activa = activa,
                                                                          controlado = controlado,
                                                                          unidadBase = unidad_base)
            print_status_message(status = sample_is_created)
            sample_history = sample_history | sample_is_created
            new_sample.save()

            new_storage, exist_storage = Almacenamiento.objects.get_or_create(idSistema = id_almacenamiento)
            print_status_message(status = exist_storage)
            sample_history = sample_history | exist_storage
            new_storage.save()

            if sample_is_created:
                new_sample.alamacenamientos.clear()
                new_sample.alamacenamientos=Almacenamiento.objects.filter(idSistema__in=alamcenamientosPosibles)
                img_url = imagen
                img_filename = urlparse(img_url).path.split('/')[-1]
                img_temp = NamedTemporaryFile()
                img_temp.write(urllib2.urlopen(img_url).read())
                img_temp.flush()
                new_sample.imagen.save(img_filename, File(img_temp))
                new_tray, tray_is_created = Bandeja.objects.get_or_create(almacenamiento = new_storage,
                                                                          posicion = posicion)
                print_status_message(status = tray_is_created)
                sample_history = sample_history | exist_storage
                for i in range (1,6):                    
                    new_muestra_bandeja, muestra_bandeja_is_created = MuestraEnBandeja.objects.get_or_create(
                            idBandeja = new_tray,
                            idMuestra = new_sample,
                            posX = i,
                            posY = 1)
                    print_status_message(status = muestra_bandeja_is_created)
                    sample_history = sample_history | muestra_bandeja_is_created
                    new_muestra_bandeja.save()
                
    if sample_history:
        return 0
    return 1


def crear_proyectos():
    project_history = False
    print ('Crear Proyectos'),
    new_project, project_is_created = Proyecto.objects.get_or_create(nombre = 'Colombia Viva')
    project_history = project_history | project_is_created

    new_project.descripcion = 'Proyecto para sintetizar una droga que reduzca el cansancio.'
    new_project.objetivo = 'Crear NZT'
    new_project.lider = Usuario.objects.get(nombre_usuario = 'acastro')
    asistentes = Usuario.objects.all().filter(nombre_usuario__startswith = 'mgalindo')
    asistentes = list(asistentes)
    new_project.asistentes.add(*asistentes)
    new_project.activo = True
    new_project.save()

    print_status_message(status = project_is_created)
    if project_history:
        return 0
    return 1


def crear_experimentos():
    experiment_history = False
    print('Crear Experimento'),

    new_experiment, experiment_is_created = Experimento.objects.get_or_create(nombre = 'Experimento Colombia Viva')
    print_status_message(status = experiment_is_created)
    experiment_history = experiment_history | experiment_is_created

    new_experiment.descripcion = 'Experimento que hace parte de Colombia Viva'
    new_experiment.objetivo = 'Crear'
    protocolos = Protocolo.objects.all()
    protocolos = list(protocolos)
    new_experiment.protocolos.add(*protocolos)
    new_experiment.proyecto = Proyecto.objects.get(nombre = 'Colombia Viva')
    new_experiment.save()

    if experiment_history:
        return 0
    return 1


def crear_protocolos():
    protocol_history = False
    print('Crear Protocolos'),

    new_protocol, protocol_is_created = Protocolo.objects.get_or_create(nombre = 'Protocolo Colombia Viva')
    print_status_message(status = protocol_is_created)
    protocol_history = protocol_history | protocol_is_created

    new_protocol.descripcion = 'Protocolo que hace parte de Colombia Viva'
    new_protocol.objetivo = 'Crear'
    new_protocol.save()

    if protocol_history:
        return 0
    return 1


def crear_pasos():
    step_history = False
    print ('Crear Pasos'),

    new_step, step_is_created = Paso.objects.get_or_create(nombre = 'Paso Colombia Viva')
    print_status_message(status = step_is_created)
    step_history = step_history | step_is_created

    new_step.descripcion = 'Paso que hace parte de Colombia Viva'
    new_step.objetivo = 'Crear'
    protocolo = Protocolo.objects.get(nombre = 'Protocolo Colombia Viva')
    new_step.protocolo = protocolo
    new_step.save()

    if step_history:
        return 0
    return 1


def crear_grupos():
    group_history = False
    print('Crear Grupos'),

    new_scientist_g, scientist_g_is_created = Group.objects.get_or_create(name = 'Científico Experimentado')
    print_status_message(status = scientist_g_is_created)
    group_history = group_history | scientist_g_is_created

    new_assistant_g, assistant_g_is_created = Group.objects.get_or_create(name = 'Asistente de Laboratorio')
    print_status_message(status = assistant_g_is_created)
    group_history = group_history | assistant_g_is_created

    new_chief_g, chief_g_is_created = Group.objects.get_or_create(name = 'Jefe de Laboratorio')
    print_status_message(status = chief_g_is_created)
    group_history = group_history | chief_g_is_created

    new_scientist_g.permissions.add(
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

    new_chief_g.permissions.add(
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

    new_assistant_g.permissions.add(
            can_listMachine,
            can_viewMachine,
            can_requestMachine,
            can_listSample,
            can_viewSample,
            can_requestSample,
            can_listRequest,
    )

    if group_history:
        return 0
    return 1


def crear_asistentes(user, num, tipo_documento, asistentes):
    assistant_history = False
    print ('Crear Asistentes'),

    new_assistant, assistant_is_created = User.objects.get_or_create(
            username = user + str(num))
    print_status_message(status = assistant_is_created)
    assistant_history = assistant_history | assistant_is_created

    if assistant_is_created:
        new_assistant.email = user + str(num) + '@uniandes.edu.co'
        new_assistant.set_password(CONTRASENA)
        new_assistant.groups.add(asistentes)
        new_assistant.save()

        new_user, user_is_created = Usuario.objects.get_or_create(
                nombre_usuario = user + str(num),
                correo_electronico = user + str(num) + '@uniandes.edu.co',
                codigo_usuario = '19950914' + str(num),
                nombres = 'Monica',
                apellidos = 'Galindo',
                telefono = '7453698',
                userNatIdTyp = tipo_documento,
                userNatIdNum = '31852496',
                grupo = asistentes,
                user = new_assistant,
                contrasena = CONTRASENA,
        )
        print_status_message(status = user_is_created)
        assistant_history = assistant_history | user_is_created
    if assistant_history:
        print ('Asistentes Creadas')
    print ('Asistentes Existentes')


def crear_usuarios():
    user_history = False
    print ('Crear Usuarios'),

    new_scientist_g, scientist_g_is_created = Group.objects.get_or_create(name = 'Científico Experimentado')
    print_status_message(status = scientist_g_is_created)
    user_history = user_history | scientist_g_is_created

    new_assistant_g, assistant_g_is_created = Group.objects.get_or_create(name = 'Asistente de Laboratorio')
    print_status_message(status = assistant_g_is_created)
    user_history = user_history | assistant_g_is_created

    new_chief_g, chief_g_is_created = Group.objects.get_or_create(name = 'Jefe de Laboratorio')
    print_status_message(status = chief_g_is_created)
    user_history = user_history | chief_g_is_created

    new_doc_type, doc_type_is_created = TipoDocumento.objects.get_or_create(nombre_corto = 'CC')
    print_status_message(status = doc_type_is_created)
    user_history = user_history | doc_type_is_created

    new_scientist, scientist_is_created = User.objects.get_or_create(username = 'acastro')

    if scientist_is_created:
        new_scientist.email = 'acastro@uniandes.edu.co'
        new_scientist.set_password(CONTRASENA)
        new_scientist.groups.add(new_scientist_g)
        new_scientist.save()

    new_user, user_is_created = Usuario.objects.get_or_create(
            nombre_usuario = 'acastro',
            correo_electronico = 'acastro@uniandes.edu.co',
            codigo_usuario = '19950912',
            nombres = 'Aquiles',
            apellidos = 'Castro',
            telefono = '7453694',
            userNatIdTyp = new_doc_type,
            userNatIdNum = '79325416',
            grupo = new_scientist_g,
            user = new_scientist,
            contrasena = CONTRASENA,
    )
    print_status_message(status = user_is_created)
    user_history = user_history | user_is_created

    new_chief, chief_is_created = User.objects.get_or_create(username = 'bcamelas')
    if chief_is_created:
        new_chief.email = 'bcamelas@uniandes.edu.co'
        new_chief.set_password(CONTRASENA)
        new_chief.groups.add(new_chief_g)
        new_chief.save()

    new_user, user_is_created = Usuario.objects.get_or_create(
            nombre_usuario = 'bcamelas',
            correo_electronico = 'bcamelas@uniandes.edu.co',
            codigo_usuario = '19950913',
            nombres = 'Benito',
            apellidos = 'Camelas',
            telefono = '7453619',
            userNatIdTyp = new_doc_type,
            userNatIdNum = '79163482',
            grupo = new_chief_g,
            user = new_chief,
            contrasena = CONTRASENA,
    )
    print_status_message(status = user_is_created)
    user_history = user_history | user_is_created

    for i in range(10):
        crear_asistentes('mgalindo', i, new_doc_type, new_assistant_g)

    new_admin = User.objects.get(username = SUPERUSUARIO)
    new_user, user_is_created = Usuario.objects.get_or_create(
            nombre_usuario = SUPERUSUARIO,
            correo_electronico = EMAIL_HOST_USER,
            codigo_usuario = '100000',
            nombres = 'Administrador',
            apellidos = 'Administrador',
            telefono = '100000',
            userNatIdTyp = new_doc_type,
            userNatIdNum = '1000000',
            grupo = new_scientist_g,
            user = new_admin,
            contrasena = CONTRASENA,
    )
    print_status_message(status = user_is_created)
    user_history = user_history | user_is_created

    if user_history:
        return 0
    return 1


class Command(BaseCommand):
    help = 'Esto crea un set de datos básico'

    def handle(self, *args, **options):

        def execute_function(me, function_name, result_text):

            if globals()[function_name]() == 0:
                me.stdout.write(me.style.SUCCESS('Al menos un "%sCreados."' % result_text))
            else:
                me.stdout.write(me.style.NOTICE('"%sYa Exsitian."' % result_text))

        lista_instalacion = [['crear_tipos_documento', 'Tipos de Documentos '],
                             ['crear_laboratorios', 'Laboratorios '],
                             ['crear_maquinas', 'Maquinas '],
                             ['crear_grupos', 'Grupos '],
                             ['crear_usuarios', 'Usuarios '],
                             ['crear_bandeja', 'Bandejas '],
                             ['crear_almacenamientos', 'Almacenamientos '],
                             ['crear_muestras', 'Muestras '],
                             ['crear_proyectos', 'Proyectos '],
                             ['crear_protocolos', 'Protocolos '],
                             ['crear_experimentos', 'Experimentos '],
                             ['crear_pasos', 'Pasos '],
                             ]

        for functions in lista_instalacion:
            execute_function(self, function_name = functions[0], result_text = functions[1])
