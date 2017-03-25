from django.core.management.base import BaseCommand
from django.templatetags.static import static
from LabModule.models import Cargo
from LabModule.models import TipoDocumento
from LabModule.models import MaquinaProfile
from LabModule.models import LaboratorioProfile
from LabModule.models import MaquinaEnLab

import json

def crearTiposDocumento():
    nuevoTipoDoc, tipoDocExistente = TipoDocumento.objects.get_or_create(nombre_corto='CC')
    if tipoDocExistente:
        nuevoTipoDoc.descripcion = 'Cedula de Ciudadania'
        nuevoTipoDoc.save()
        return 0
    return 1


def crearCargos():
    nuevoCargo, cargoExistente = Cargo.objects.get_or_create(nombre_cargo='Cientifico Experimentado')
    if nuevoCargo:
        nuevoCargo.save()
        return 0
    return 1


def crearLaboratorio():

    nuevoLab, laboratioExistente=LaboratorioProfile.objects.get_or_create(nombre="Laboratorio principal",id="LAB001")
    if laboratioExistente:
        return 0
    return 1


def crearMaquina():
    nuevoLab, laboratioExistente=LaboratorioProfile.objects.get_or_create(nombre="Laboratorio principal",id="LAB001")
    rta=1
    with open(".///"+static('lab_static/json/maquinas.json')) as data_file:
        data = json.load(data_file) 
        for maquina in data:
            nuevaMaquina, maquinaExistente=MaquinaProfile.objects.get_or_create(nombre=maquina['nombre'],
                descripcion=maquina['descripcion'],
                idSistema=maquina['idSistema'],
                con_reserva=maquina['con_reserva']
                )
            nuevare,exre=MaquinaEnLab.objects.get_or_create(idLaboratorio=nuevoLab,idMaquina=nuevaMaquina,
                    xPos=maquina['x'],yPos=maquina['y'])
            if maquinaExistente: 
                rta=0    
    return rta


def crearBandeja():
    return 0


def crearAlmacenamiento():
    return 0


def crearMuestra():
    return 0


def crearProyecto():
    return 0


def crearExperimento():
    return 0


def crearProtocolo():
    return 0


def crearPaso():
    return 0


class Command(BaseCommand):
    help = 'Esto crea un set de datos basico'

    def handle(self, *args, **options):
        if (crearTiposDocumento() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Tipos de Documentos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Tipos de Documentos '))
        if (crearCargos() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Cargos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Cargos '))
        if (crearLaboratorio() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Laboratorios '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Laboratorios '))
        if (crearMaquina() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Maquinas '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Maquinas '))
        if (crearBandeja() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Bandejas '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Bandejas '))
        if (crearAlmacenamiento() == 0):
            self.stdout.write(self.style.SUCCESS('"%sCreados."' % 'Almacenamientos '))
        else:
            self.stdout.write(self.style.NOTICE('"%sYa Exsitian."' % 'Almacenamientos '))
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