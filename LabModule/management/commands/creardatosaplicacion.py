# -*- coding: utf-8 -*-
import json
import urllib ,urllib2 
from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.templatetags.static import static
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from LabModule.models import LaboratorioProfile
from LabModule.models import MaquinaEnLab
from LabModule.models import MaquinaProfile
from LabModule.models import TipoDocumento
from LabModule.models import Usuario
from LabModule.models import Proyecto
from LabModule.models import LugarAlmacenamientoEnLab
from LabModule.models import LugarAlmacenamiento
from LabModule.models import Muestra
from LabModule.models import Bandeja
CONTRASENA = getattr(settings, "CONTRASENA", '1a2d3m4i5n6')


def crearTiposDocumento():
    nuevoTipoDoc, tipoDocExistente = TipoDocumento.objects.get_or_create(nombre_corto = 'CC')
    if tipoDocExistente:
        nuevoTipoDoc.descripcion = 'Cedula de Ciudadania'
        nuevoTipoDoc.save()
        return 0
    return 1


def crearLaboratorio():
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio principal",
                                                                            id = "LAB001")
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio Secundario",
                                                                            id = "LAB002")
    nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(nombre = "Laboratorio Terciario",
                                                                            id = "LAB003")
    if laboratioExistente:
        return 0
    return 1


def crearMaquina():
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
            nuevare, exre = MaquinaEnLab.objects.get_or_create(idLaboratorio = nuevoLab,
                                                               idMaquina = nuevaMaquina,
                                                               posX = maquina['x'],
                                                               posY = maquina['y'])
            if maquinaExistente:
                rta = 0
    return rta


def crearBandeja():
    return 0


def crearAlmacenamiento():
    rta=1
    with open(".///" + static('lab_static/json/lugares.json')) as data_file:
        data=json.load(data_file)
        idAct=0

        for row in data: 
            nombre=row['nombre']
            descripcion=row['descripcion']
            capacidad=row['capacidad']
            temperatura=row['temperatura']
            estado=row['estado']
            imagen=row['imagen']
            cantidad=row['cantidad']
            posX=row['posX']
            posY=row['posY']
            idLaboratorio=row['idLaboratorio']
            nuevoLab, laboratioExistente = LaboratorioProfile.objects.get_or_create(id = idLaboratorio)
            img_url = imagen
            img_filename = urlparse(img_url).path.split('/')[-1]
            img_temp = NamedTemporaryFile()
            img_temp.write(urllib2.urlopen(img_url).read())
            img_temp.flush()
            for i in range(1,int(cantidad)+1):
                    idAct+=1
                    nuevoLugar, luarCreado = LugarAlmacenamiento.objects.get_or_create(nombre=nombre+" "+str(i),descripcion=descripcion,capacidad=capacidad,
                        temperatura=temperatura,estado=estado,id="LUGAR"+str(idAct))
                    nuevoLugar.imagen.save(img_filename, File(img_temp))      
                    print ("creando",nombre+" "+str(i))
                    if  luarCreado:
                        rta=0
                        xPos=int(posX)+(i-1)
                        yPos=int(posY)
                        if xPos>10:
                            xPos=xPos-10
                            yPos=yPos+1
                        nuevloLugarEnLab,lugarENLabExistente=LugarAlmacenamientoEnLab.objects.get_or_create(idLaboratorio=nuevoLab,idLugar=nuevoLugar,posX=xPos,posY=yPos)
    return rta


def crearMuestra():
    rta=1
    with open(".///" + static('lab_static/json/muestras.json')) as data_file:
        data=json.load(data_file)
        idAct=0
        for row in data: 
            nombre=row['nombre']
            descripcion=row['descripcion'] 
            Tipo=row['Tipo'] 
            valor=row['valor'] 
            activa=row['activa']  
            controlado=row['controlado']  
            imagen=row['imagen']
            unidadBase=row['unidadBase']  
            idAlmacenamiento=row['idAlmacenamiento']
            nuevaMuestra, mustraCreada = Muestra.objects.get_or_create(nombre=nombre,descripcion=descripcion,valor=valor,activa=activa,controlado=controlado,
                unidadBase=unidadBase)
            nuevoLugar,LugarExistente=LugarAlmacenamiento.objects.get_or_create(id=idAlmacenamiento)
            if mustraCreada:
                print("Creando muestra",nombre)
                rta=0
                img_url = imagen
                img_filename = urlparse(img_url).path.split('/')[-1]
                img_temp = NamedTemporaryFile()
                img_temp.write(urllib2.urlopen(img_url).read())
                img_temp.flush()
                nuevaMuestra.imagen.save(img_filename, File(img_temp))
                cuenta=Bandeja.objects.filter(lugarAlmacenamiento = nuevoLugar).count()
                posicion = 1 if cuenta==0 else cuenta+1
                nuevaBandeja,bandejaExistenet=Bandeja.objects.get_or_create(muestra=nuevaMuestra,lugarAlmacenamiento=nuevoLugar,posicion=posicion)

                
    return rta


def crearProyecto():
    nuevoProyecto,noexistia=Proyecto.objects.get_or_create(nombre="Colombia Viva")
    
    nuevoProyecto.descripcion="Proyecto para sintetizar una droga que reduzca el cansancio"
    nuevoProyecto.objetivo="Crear"
    nuevoProyecto.lider=Usuario.objects.get(nombre_usuario='acastro')
    nuevoProyecto.asistentes=[Usuario.objects.get(nombre_usuario='mgalindo')]
    nuevoProyecto.activo=True
    return 0

    return 1


def crearExperimento():
    return 0


def crearProtocolo():
    return 0


def crearPaso():
    return 0


def createGroups():
    cientificos, created1 = Group.objects.get_or_create(name = 'Cientifico Experimentado')
    asistentes, created2 = Group.objects.get_or_create(name = 'Asistente de Laboratorio')
    jefes, created3 = Group.objects.get_or_create(name = 'Jefe de Laboratorio')

    maquinasAgregar = Permission.objects.get(name='maquina||agregar')
    maquinasEditar = Permission.objects.get(name='maquina||editar')
    maquinasVer = Permission.objects.get(name='maquina||ver')
    maquinasSolicitar = Permission.objects.get(name='maquina||solicitar')
    agregarUsuario = Permission.objects.get(name='usuario||agregar')

    cientificos.permissions.add(maquinasAgregar, maquinasEditar, maquinasVer, agregarUsuario)
    jefes.permissions.add(maquinasVer, agregarUsuario)
    asistentes.permissions.add(maquinasVer)
    asistentes.permissions.add(maquinasSolicitar)
    if created1 or created2 or created3:
        return 0
    return 1


def createUsers():
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
    else:
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

    exist_jefe, new_jefe = User.objects.get_or_create(username = 'bcamelas')
    if new_jefe:
        exist_jefe.email = 'bcamelas@uniandes.edu.co'
        exist_jefe.set_password(CONTRASENA)
        exist_jefe.groups.add(jefes)
        exist_jefe.save()
    else:
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

    exist_asistente, new_asistente = User.objects.get_or_create(
            username = 'mgalindo')
    if new_asistente:
        exist_asistente.email = 'mgalindo@uniandes.edu.co'
        exist_asistente.set_password(CONTRASENA)
        exist_asistente.groups.add(asistentes)
        exist_asistente.save()
    else:
        exist_asistente.email = 'mgalindo@uniandes.edu.co'
        exist_asistente.set_password(CONTRASENA)
        exist_asistente.groups.add(asistentes)
        exist_asistente.save()

    exist_usuario, new_usuario = Usuario.objects.get_or_create(
            nombre_usuario = 'mgalindo',
            correo_electronico = 'mgalindo@uniandes.edu.co',
            codigo_usuario = '19950914',
            nombres = 'Monica',
            apellidos = 'Galindo',
            telefono = '7453698',
            userNatIdTyp = tipDocumento,
            userNatIdNum = '31852496',
            grupo = asistentes,
            user = exist_asistente,
            contrasena = CONTRASENA,
    )

    if new_cientifico or new_jefe or new_asistente:
        return 0
    return 1


class Command(BaseCommand):
    help = 'Esto crea un set de datos basico'

    def handle(self, *args, **options):
        if (crearTiposDocumento() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Tipos de Documentos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Tipos de Documentos '))
        if (crearLaboratorio() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Laboratorios '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Laboratorios '))
        if (crearMaquina() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Maquinas '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Maquinas '))

        if (createGroups() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Grupos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Grupos '))
        if (createUsers() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Usuarios '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Usuarios '))

        if (crearBandeja() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Bandejas '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Bandejas '))
        # if (crearAlmacenamiento() == 0):
        #     self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Almacenamientos '))
        # else:
        #     self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Almacenamientos '))
        if (crearMuestra() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Muestras '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Muestras '))
        if (crearProyecto() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Proyectos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Proyectos '))
        if (crearExperimento() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Experimentos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Experimentos '))
        if (crearProtocolo() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Protocolos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Protocolos '))
        if (crearPaso() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Pasos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Pasos '))
