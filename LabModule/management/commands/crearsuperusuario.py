from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

SUPERUSUARIO = getattr(settings, "SUPERUSUARIO", 'admin')
CONTRASENA = getattr(settings, "CONTRASENA", '1a2d3m4i5n6')
EMAIL_HOST_USER = getattr(settings, "EMAIL_HOST_USER", 'admin@admin.com')


def crearsuperusuario():
    username = SUPERUSUARIO
    password = CONTRASENA
    email = EMAIL_HOST_USER

    if User.objects.filter(username=username).count() == 0:
        User.objects.create_superuser(username, email, password)
        return 0
    else:
        return 1


def createGroups():
    cientificos, created1 = Group.objects.get_or_create(name='cientificos')
    asistentes, created2 = Group.objects.get_or_create(name='asistentes')
    jefes, created3 = Group.objects.get_or_create(name='jefes de laboratorio')

    maquinasAgregar = Permission.objects.get(name='maquina||agregar')
    maquinasEditar = Permission.objects.get(name='maquina||editar')
    maquinasVer = Permission.objects.get(name='maquina||ver')
    agregarUsuario = Permission.objects.get(name='usuario||agregar')

    cientificos.permissions.add(maquinasAgregar, maquinasEditar, maquinasVer, agregarUsuario)
    jefes.permissions.add(maquinasVer, agregarUsuario)
    asistentes.permissions.add(maquinasVer)
    if created1 or created2 or created3:
        return 0
    return 1


def createUsers():
    cientificos = Group.objects.get(name='cientificos')
    asistentes = Group.objects.get(name='asistentes')
    jefes = Group.objects.get(name='jefes de laboratorio')

    cientifico, cientificoCreado = User.objects.get_or_create(
        username='cientifico')
    if cientificoCreado:
        cientifico.email = 'j@a.com'
        cientifico.set_password(CONTRASENA)
        cientifico.groups.add(cientificos)
        cientifico.save()

    jefe, jefeCreado = User.objects.get_or_create(
        username='jefe')
    if jefeCreado:
        jefe.email = 'j@a.com'
        jefe.set_password(CONTRASENA)
        jefe.groups.add(jefes)
        jefe.save()

    assistente, assistenteCreado = User.objects.get_or_create(
        username='asistente')
    if assistenteCreado:
        assistente.email = 'j@a.com'
        assistente.set_password(CONTRASENA)
        assistente.groups.add(asistentes)
        assistente.save()

    if cientificoCreado or jefeCreado or assistenteCreado:
        return 0
    return 1


class Command(BaseCommand):
    help = 'Configuracion Inicial SuperUsuario'

    def handle(self, *args, **options):
        if (crearsuperusuario() == 0):
            self.stdout.write(self.style.SUCCESS('Superusuario creado.'))
        else:
            self.stdout.write(self.style.NOTICE('Superusuario ya existia.'))
        if (createGroups() == 0):
            self.stdout.write(self.style.SUCCESS('Grupos creados'))
        else:
            self.stdout.write(self.style.NOTICE('Los grupos ya existian.'))

        if (createUsers() == 0):
            self.stdout.write(self.style.SUCCESS('Usuarios creados'))
        else:
            self.stdout.write(self.style.NOTICE('Los usuarios ya existian.'))
