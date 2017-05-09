# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from registration.backends.default.views import RegistrationView

from LabModule.app_forms.Usuario import RegistroUsuarioForm


class UserRegistrationView(RegistrationView):
    """Clase para el funcionamiento del regitro de usuario
            Historia de usuario: ALF-15:Yo como Usuario quiero ingresar al sistema con mis credenciales para acceder a
            todas las funcionalidades que el mismo tiene para mi.
            Se encarga de:
                * Ayuda al modelo de vista para renderizar la información del usuario
            :param RegistrationView: Clase que ayuda al modulo de registro de usuarios
            :type RegistrationView: RegistrationView.
        """
    form_class = RegistroUsuarioForm


@csrf_exempt
def registrar_usuario(request):
    """Registro de Usuarios
            Historia de usuario: ALF-15:Yo como Usuario quiero ingresar al sistema con mis credenciales para acceder
            a todas las funcionalidades que el mismo tiene para mi.
            Se encarga de:
                * Obtiene el formulario en el request
                * crea un usuario y un perfil
        :param request: El HttpRequest que se va a responder.
        :type request: HttpRequest.
        :returns: HttpResponse -- La respuesta a la peticion si sale bien, al home, sino al mismo formulario,
        si no tiene permisos responde no autorizado
       """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addUser"):
        section = {'title': _('Agregar Usuario')}
        form = RegistroUsuarioForm(request.POST or None)
        if form.is_valid():
            nuevo_usuario = form.save(commit = False)
            try:
                nuevo_perfil = User.objects.create_user(username = nuevo_usuario.nombre_usuario,
                                                        email = nuevo_usuario.correo_electronico,
                                                        password = nuevo_usuario.contrasena,
                                                        first_name = nuevo_usuario.nombres,
                                                        last_name = nuevo_usuario.apellidos
                                                        )
                nuevo_usuario.user = nuevo_perfil
                nuevo_usuario.user.groups.add(nuevo_usuario.grupo)
                nuevo_usuario.save()
                return HttpResponseRedirect(reverse('home'))
            except:
                form.add_error("userCode", _("Un usuario con este id ya existe"))
        context = {'form': form, 'section': section}
        return render(request, 'registration/registration_form.html', context)
    return HttpResponse(_('No autorizado'), status = 401)
