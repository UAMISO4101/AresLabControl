from django.conf import settings
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


class Command(BaseCommand):
    help = 'Configuracion Inicial SuperUsuario'

    def handle(self, *args, **options):
        if (crearsuperusuario() == 0):
            self.stdout.write(self.style.SUCCESS('Superusuario creado.'))
        else:
            self.stdout.write(self.style.NOTICE('Superusuario ya existia.'))
