from django.core.management.base import BaseCommand

from LabModule.models import Cargo
from LabModule.models import TipoDocumento


def crearTiposDocumento():
    nuevoTipoDoc, tipoDocExistente = TipoDocumento.objects.get_or_create(nombre_corto='CC')
    if nuevoTipoDoc:
        nuevoTipoDoc.descripcion = 'Cedula de Ciudadania'
        nuevoTipoDoc.save()
        return 0
    return 1


def crearCargos():
    nuevoCargo, cargoExistente = Cargo.objects.get_or_create(nombre_cargo='Cientifico Experimentado')
    if nuevoCargo:
        nuevoCargo.save()
        return 0
    return 0


def crearLaboratorio():
    return 0


def crearMaquina():
    return 0


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
