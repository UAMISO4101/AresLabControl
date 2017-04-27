# -*- coding: utf-8 -*-
from __future__ import print_function

import json

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from registration.backends.default.views import RegistrationView

from forms import MaquinaForm
from forms import MuestraForm
from forms import PosicionesAlmacenamientoForm
from forms import PosicionesMaquinaForm
from models import Bandeja
from models import Experimento
from models import LaboratorioProfile
from models import LugarAlmacenamiento
from models import LugarAlmacenamientoEnLab
from models import MaquinaEnLab
from models import MaquinaProfile
from models import MaquinaSolicitud
from models import Muestra
from models import MuestraSolicitud
from models import Paso
from models import Protocolo
from models import Proyecto
from models import Solicitud
from models import Usuario
from .forms import LugarAlmacenamientoForm
from .forms import MuestraSolicitudForm
from .forms import RegistroUsuarioForm
from .forms import SolicitudForm
from django.contrib import messages


# Create your views here.
def home(request):
    """Metodo inicial de la aplicación
               Se encarga de:
                   * Mostrar el inicio de la aplicación
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :returns: HttpResponse -- La respuesta redirigiendo a la página home inicial de la aplicación
        """
    context = {}
    return render(request, "home.html", context)


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


def lugar_add(request):
    """Desplegar y comprobar los valores a insertar.
           Historia de usuario: ALF-37 - Yo como Jefe de Laboratorio quiero poder agregar nuevos lugares de
           almacenamiento para poder utilizarlos en el sistema.
           Se encarga de:
               * Mostar el formulario para agregar un lugar de almacenamiento.
               * Mostar el formulario para editar un lugar de almacenamiento ya existente.
               * Agregar un lugar de almacenamiento a la base de datos, agregar la relación entre lugar de
               almacenamiento y el laboratorio en el que está.
        :param request: El HttpRequest que se va a responder.
        :type request: HttpRequest.
        :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a la
        modificación del lugar de almacenamiento. Sino redirecciona al mismo formulario mostrando los errores.
       """
    section = {'title': 'Agregar Lugar de Almacenamiento'}
    mensaje = ""
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = LugarAlmacenamientoForm(request.POST or None, request.FILES or None)
            formPos = PosicionesAlmacenamientoForm(request.POST or None, request.FILES or None)

            if form.is_valid() and formPos.is_valid():
                lugar = form.save(commit = False)
                lugarEnLab = formPos.save(commit = False)

                ocupado = MaquinaEnLab.objects.filter(idLaboratorio = lugarEnLab.idLaboratorio, posX = lugarEnLab.posX,
                                                      posY = lugarEnLab.posY).exists()

                if ocupado:
                    formPos.add_error("posX", "La posición x ya esta ocupada")
                    formPos.add_error("posY", "La posición y ya esta ocupada")

                    mensaje = "El lugar en el que desea guadar ya esta ocupado"
                else:
                    mensaje = "La posición [" + str(lugarEnLab.posX) + "," + str(
                            lugarEnLab.posY) + "] no se encuentra en el rango del laboratorio"
                    lab = lugarEnLab.idLaboratorio
                    masX = lab.numX >= lugarEnLab.posX
                    masY = lab.numY >= lugarEnLab.posY
                    posible = masX and masY
                    if not posible:
                        if not masX:
                            formPos.add_error("posX", "La posición x sobrepasa el valor máximo de " + str(lab.numX))
                        if not masY:
                            formPos.add_error("posY", "La posición y sobrepasa el valor máximo de " + str(lab.numY))
                    else:
                        if lugar.capacidad<=0:
                            form.add_error("capacidad", "La capacidad debe ser mayor a cero")
                            mensaje = "La capacidad del lugar de almacenamiento debe ser mayor a cero"
                        else:
                            lugar.save()
                            lugarEnLab.idLugar = lugar
                            lugarEnLab.save()

                            for cantidad in range(lugar.capacidad):
                                bandeja = Bandeja(lugarAlmacenamiento = lugar,
                                                  libre = True, posicion = cantidad)
                                bandeja.save()
                            messages.success(request, "El lugar se añadio exitosamente")
                            return HttpResponseRedirect(reverse('lugar-detail', kwargs = {'pk': lugar.pk}))
        else:
            form = LugarAlmacenamientoForm()
            formPos = PosicionesAlmacenamientoForm()
        context = {'form': form, 'formPos': formPos, 'mensaje': mensaje, 'section': section}

        return render(request, 'almacenamientos/agregar.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def comprobarPostMaquina(form, formPos, request, template_name, section):
    """Desplegar y comprobar los valores a insertar.
        Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :
        Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
        Se encarga de:
            * Mostar el formulario para agregar una máquina.
            * Mostar el formulario para editar una máquina ya existente.
            * Agregar una máquina a la base de datos, agregar la relación entre la máquina y el
            laboratorio en el que está.
     :param form: La información relevante de la máquina.
     :type form: MaquinaForm.
     :param formPos: La posición y el laboratorio en el que se va a guardar la máquina.
     :type formPos: PosicionesMaquinaForm.
     :param request: El HttpRequest que se va a responder.
     :type request: HttpRequest.
     :param template_name: La template sobre la cual se va a renderizar.
     :type template_name: html.
     :param section: Objeto que permite diferenciar entre la modificación de una máquina y la adición de esta.
     :type section: {‘title’:,’agregar’}.
     :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a la
      modificación de la nueva máquina. Sino redirecciona al mismo formulario mostrand los errores.
    """

    mensaje = ""

    if form.is_valid() and formPos.is_valid():
        new_maquina = form.save(commit = False)
        new_maquinaEnLab = formPos.save(commit = False)
        posX = new_maquinaEnLab.posX
        posY = new_maquinaEnLab.posY
        ocupadoX = MaquinaEnLab.objects.filter(idLaboratorio = new_maquinaEnLab.idLaboratorio, posX = posX).exists()
        ocupadoY = MaquinaEnLab.objects.filter(idLaboratorio = new_maquinaEnLab.idLaboratorio, posY = posY).exists()
        lamisma = MaquinaEnLab.objects.filter(pk = new_maquinaEnLab.pk).exists()
        if (ocupadoX and ocupadoY) and not lamisma:
            if (ocupadoX):
                formPos.add_error("posX", "La posición x ya esta ocupada")
            if (ocupadoY):
                formPos.add_error("posY", "La posición y ya esta ocupada")
            mensaje = "El lugar en el que desea guadar ya esta ocupado"
        else:
            mensaje = "La posición [" + str(posX) + "," + str(posY) + "] no se encuentra en el rango del labortorio"
            lab = new_maquinaEnLab.idLaboratorio
            masX = lab.numX >= posX
            masY = lab.numY >= posY
            posible = masX and masY
            if not posible:
                if not masX:
                    formPos.add_error("posX", "La posición x sobrepasa el valor máximo de " + str(lab.numX))
                if not masY:
                    formPos.add_error("posY", "La posición y sobrepasa el valor máximo de " + str(lab.numY))
            else:
                new_maquina.save()
                new_maquinaEnLab.idMaquina = new_maquina
                new_maquinaEnLab.save()
                if section['agregar']:
                    messages.success(request, "La máquina se añadio exitosamente")
                else:
                    messages.success(request, "La máquina se actualizo correctamente")
                return redirect(reverse('maquina-update', kwargs = {'pk': new_maquina.pk}))

    return render(request, template_name,
                  {'form': form, 'formPos': formPos, 'section': section, 'mensaje': mensaje})


def maquina_add(request, template_name = 'maquinas/agregar.html'):
    """Comporbar si el usuario puede agregar una máquina y obtener los campos necesarios.
        Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :
        Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
        Se encarga de:
            * Comprobar si hay un usario logeuado
            * Comprobar si el suario tiene permisos para agregar máquinas
            * Obtener los campos y archivos para redireccionarlos a :func:`comprobarPostMaquina` así
              como decirle el section
            * Definir el template a usar
     :param request: El HttpRequest que se va a responder.
     :type request: HttpRequest.
     :param template_name: La template sobre la cual se va a renderizar.
     :type template_name: html.
     :param section: Objeto que permite diferenciar entre la modificación de una máquina y la adición de esta.
     :type section: {‘title’:,’agregar’}.
     :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a
     la modificación de la nueva
                               máquina. Sino redirecciona al mismo formulario mostrando los errores.
                               Si no esta autorizado se envia un código 401
    """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addMachine"):
        section = {'title': 'Agregar Máquina', 'agregar': True}
        form = MaquinaForm(request.POST or None, request.FILES or None)
        formPos = PosicionesMaquinaForm(request.POST or None, request.FILES or None)
        return comprobarPostMaquina(form, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status = 401)


def maquina_detail(request, pk, template_name = 'Maquinas/detalle.html'):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewMachine"):
        maquina = get_object_or_404(MaquinaProfile, pk = pk)
        maquinaEnLab = get_object_or_404(MaquinaEnLab, idMaquina = maquina)
        mensaje = ""
        section = {'title': 'Ver detalle ', 'agregar': "ver"}
        mensajeCalendario = "Este es el horario disponible de la máquina. Seleccione el horario que más le convenga"
        return render(request, template_name,
                      {'maquina': maquina, 'maquinaEnLab': maquinaEnLab, 'section': section,
                       'mensaje': mensaje, 'mensajeCalendario': mensajeCalendario})
    else:
        return HttpResponse('No autorizado', status = 401)


def maquina_update(request, pk, template_name = 'maquinas/agregar.html'):
    """Comporbar si el usuario puede modificar una máquina, obtener los campos necesarios.
        Se encarga de:
            * Comprobar si hay un usario logeuado
            * Comprobar si el suario tiene permisos para modificar máquinas
            * Obtener los campos y archivos para redireccionarlos a :func:`comprobarPostMaquina` así
              como decirle el section
            * Definir el template a usar
     :param request: El HttpRequest que se va a responder.
     :type request: HttpRequest.
     :param template_name: La template sobre la cual se va a renderizar.
     :type template_name: html.
     :param pk: La llave primaria de la máquina a modificar
     :type pk: String.
     :param section: Objeto que permite diferenciar entre la modificación de una máquina y la adición de esta.
     :type section: {‘title’:,’agregar’}.
     :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a si mismo.
     Sino redirecciona al mismo formulario mostrando los errores. Si no esta autorizado se envia un código 401
    """

    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_editMachine"):
        server = get_object_or_404(MaquinaProfile, pk = pk)
        serverRelacionLab = get_object_or_404(MaquinaEnLab, idMaquina = server)
        mensaje = ""
        form = MaquinaForm(request.POST or None, request.FILES or None, instance = server)
        formPos = PosicionesMaquinaForm(request.POST or None, request.FILES or None, instance = serverRelacionLab)
        section = {'title': 'Modificar Máquina', 'agregar': False}
        return comprobarPostMaquina(form, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status = 401)


def maquina_list(request):
    """Comprobar si el usario puede ver las máquinas y mostraselas filtrando por una búsqueda.
           Historia de usuario: ALF-20:Yo como Jefe de Laboratorio quiero poder filtrar las máquinas existentes por
           nombre para visualizar sólo las que me interesan.
           Historia de usuario: ALF-25:Yo como Asistente de Laboratorio quiero poder filtrar las máquinas existentes
           por nombre para visualizar sólo las que me interesan.
           Se encarga de:
               * Comprobar si hay un usario logueado
               * Comprobar si el suario tiene permisos para ver las máquinas
               * Obtener todas las máquinas cuyo nombre contenga el párametro solicitado por el usario
               * Páginar el resultado de la consulta.

        :param pag: Opcional: El número de página que se va a mostrar en la páginación.
        :type pag: Integer.
        :param que: Opcional: La búsqueda que se va a realizar
        :type que: String.
        :param num: Opcional: El número de máquinas a ver en cada página
        :type num: String.
        :returns: HttpResponse -- La respuesta a la petición. Retorna páginada la lista de las máquias que cumplen
         con la búsqueda. Si no esta autorizado se envia un código 401
    """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewMachine"):
        section = {}
        section['title'] = 'Listar Máquinas'
        edita = request.user.has_perm("LabModule.can_editMachine")
        if not edita:
            lista_maquinas = MaquinaProfile.objects.all().filter(activa = True).extra(order_by = ['nombre'])
        else:
            lista_maquinas = MaquinaProfile.objects.all().extra(order_by = ['nombre'])

        id_maquina = [maquina.idSistema for maquina in lista_maquinas]
        lista_Posiciones = MaquinaEnLab.objects.all().filter(idMaquina__in = id_maquina)
        maquinasConUbicacion = zip(lista_maquinas, lista_Posiciones)
        context = {'section': section, 'maquinasBien': maquinasConUbicacion}
        return render(request, 'maquinas/listar.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def lugar_list(request):
    """Desplegar y comprobar los valores a consultar.
              Historia de usuario: ALF-39 - Yo como Jefe de Laboratorio quiero poder filtrar los lugares de
              almacenamiento existentes por nombre para visualizar sólo los que me interesan.
              Se encarga de:
                  * Mostar el formulario para consultar los lugares de almacenamiento.
           :param request: El HttpRequest que se va a responder.
           :type request: HttpRequest.
           :returns: HttpResponse -- La respuesta a la petición, con información de los lugares de
           almacenamiento existentes.
          """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewStorage"):
        section = {}
        section['title'] = 'Listar Almacenamientos'
        edita = request.user.has_perm("LabModule.can_editStorage")
        if not edita:
            lista_almacenamiento = LugarAlmacenamiento.objects.all().filter(activa = True).extra(order_by = ['nombre'])
        else:
            lista_almacenamiento = LugarAlmacenamiento.objects.all().extra(order_by = ['nombre'])

        id_almacenamiento = [maquina.id for maquina in lista_almacenamiento]
        lista_Posiciones = LugarAlmacenamientoEnLab.objects.all().filter(idLugar__in = id_almacenamiento)
        lugaresConUbicacion = zip(lista_almacenamiento, lista_Posiciones)
        context = {'section': section, 'lista_lugares': lugaresConUbicacion}
        return render(request, 'almacenamientos/listar.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def maquina_request(request):
    """Realiza la solicitud de máquinas por el usuario que la necesita
        Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una
        franja de tiempo especifica para hacer uso de ella
        Se encarga de:
            * Comprobar si hay un usuario logueado
            * Comprobar si el usuario tiene permisos para realizar la solicitud de máquinas
            * Realizar la solicitud de máquinas
     :param request: El HttpRequest que se va a responder.
     :type request: HttpRequest.
     :returns: HttpResponse -- La respuesta a la petición. Si no esta autorizado se envia un código 401
    """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_requestMachine"):
        mensaje = 'ok'
        contexto = {'start': request.GET.get('start', ''), 'end': request.GET.get('end', '')}

        try:

            maquina = MaquinaProfile.objects.get(pk = request.GET.get('id', 0), activa = True)
            profile = Usuario.objects.get(user_id = request.user.id)
            maquinaEnLab = MaquinaEnLab.objects.get(idMaquina = maquina.pk)
            proyectos = Proyecto.objects.filter(asistentes = profile.id, activo = True)
            form = SolicitudForm()
            if request.method == 'POST':
                if form.verificar_fecha(maquina.pk, request.POST['fechaInicial'], request.POST['fechaFinal']) == True:
                    requestObj = Solicitud()
                    requestObj.descripcion = 'Solicitud de maquina'
                    requestObj.fechaInicial = request.POST['fechaInicial']
                    requestObj.fechaFinal = request.POST['fechaFinal']
                    if maquina.con_reserva == True:
                        requestObj.estado = 'creada'
                    else:
                        requestObj.estado = 'aprobada'
                    requestObj.solicitante = profile
                    requestObj.paso = Paso.objects.get(id = request.POST['step'])
                    requestObj.save()
                    maquinaRequest = MaquinaSolicitud()
                    maquinaRequest.maquina = maquina
                    maquinaRequest.solicitud = requestObj
                    maquinaRequest.save()
                    messages.success(request, "La máquina se reservo exitosamente")
                    return redirect(reverse('maquina-detail', kwargs = {'pk': request.GET.get('id', 0)}))
                else:
                    mensaje = "Ya existe una solicitud para estas fechas"

            contexto = {'form'        : form, 'mensaje': mensaje, 'maquina': maquina, 'proyectos': proyectos,
                        'maquinaEnLab': maquinaEnLab, 'start': request.GET.get('start', ''),
                        'end'         : request.GET.get('end', '')}
        except ObjectDoesNotExist as e:
            contexto = {'mensaje': 'No hay maquinas o pasos con el id solicitado'}
        except MultipleObjectsReturned as e:
            contexto = {'mensaje': 'Muchas maquinas con ese id'}
        return render(request, "solicitudes/crear_maquina_solicitud.html", contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


def lugar_detail(request, pk):
    """Desplegar y comprobar los valores a consultar.
                Historia de usuario: ALF-42-Yo como Jefe de Laboratorio quiero poder ver el detalle de un
                lugar de almacenamiento para conocer sus características
                Se encarga de:
                * Mostar el formulario para consultar los lugares de almacenamiento.
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :param pk: La llave primaria del lugar de almacenamiento
            :type pk: String.
            :returns: HttpResponse -- La respuesta a la petición, con información de los lugares de almacenamiento existentes.
        """
    if request.user.is_authenticated():
        lista_lugar = LugarAlmacenamientoEnLab.objects.filter(idLugar_id = pk)
        if lista_lugar is None:
            return lugar_list(request)
        else:
            lugar = lista_lugar[0]
            bandejasOcupadas = Bandeja.objects.filter(lugarAlmacenamiento_id = pk, libre = False).count()
            bandejasLibres = Bandeja.objects.filter(lugarAlmacenamiento_id = pk, libre = True).count()
            # tamano = 0
            # lista = Bandeja.objects.filter(lugarAlmacenamiento_id=pk)

            # for x in lista:
            # tamano += Decimal(x.tamano)

            laboratorio = LaboratorioProfile.objects.get(pk = lugar.idLaboratorio_id).nombre

            context = {'lugar'      : lugar, 'bandejasOcupadas': bandejasOcupadas, 'bandejasLibres': bandejasLibres,
                       'laboratorio': laboratorio}
            return render(request, 'almacenamientos/detalle.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def muestra_request(request):
    """Realiza la solicitud de muestras por el usuario que la necesita
            Historia de usuario: ALF-81:Yo como Asistente de Laboratorio quiero poder solicitar una muestra para
             continuar con mis experimentos
            Se encarga de:
                * Comprobar si hay un usuario logueado
                * Comprobar si el usuario tiene permisos para realizar la solicitud de muestras
                * Realizar la solicitud de muestras
         :param request: El HttpRequest que se va a responder.
         :type request: HttpRequest.
         :returns: HttpResponse -- La respuesta a la petición. Si no esta autorizado se envia un código 401
    """

    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_requestSample"):
        mensaje = 'ok'
        contexto = {}
        try:

            muestra = Muestra.objects.get(id = request.GET.get('id', 0), activa = True)
            profile = Usuario.objects.get(user_id = request.user.id)
            proyectos = Proyecto.objects.filter(asistentes = profile.id, activo = True);

            if request.method == 'POST':

                requestObj = Solicitud()
                requestObj.descripcion = 'Solicitud de uso de muestra'
                requestObj.fechaInicial = request.POST['fechaInicial']
                requestObj.estado = 'creada'
                requestObj.solicitante = profile
                requestObj.paso = Paso.objects.get(id = request.POST['step'])
                requestObj.save()
                sampleRequest = MuestraSolicitud()
                sampleRequest.solicitud = requestObj
                sampleRequest.muestra = muestra
                sampleRequest.cantidad = request.POST['cantidad']
                sampleRequest.tipo = 'uso'
                sampleRequest.save()
                return redirect(reverse('muestra-list', kwargs = {}))

            else:
                form = SolicitudForm()
                form_muestra = MuestraSolicitudForm()
            contexto = {'form'        : form, 'mensaje': mensaje, 'muestra': muestra, 'proyectos': proyectos,
                        'form_muestra': form_muestra}
        except ObjectDoesNotExist as e:
            contexto = {'mensaje': 'No hay muestras o pasos con el id solicitado'}

        except MultipleObjectsReturned as e:
            contexto = {'mensaje': 'Muchas muestras con ese id'}

        return render(request, "solicitudes/crear_muestra_solicitud.html", contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


def muestra_detail(request, pk):
    """Desplegar y comprobar los valores a consultar.
                Historia de usuario: ALF-50 - Yo como Asistente de Laboratorio quiero poder ver el detalle de una
                muestra para conocer sus características.
                Se encarga de:
                * Mostar el formulario para consultar las muestras.
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :param pk: La llave primaria de la muestra
            :type pk: String.
            :returns: HttpResponse -- La respuesta a la petición, con información de la muestra existente.
        """
    if request.user.is_authenticated():
        section = {}
        section['title'] = 'Detalles '
        lista_muestra = Muestra.objects.filter(id = pk)
        if lista_muestra is None:
            return muestra_list(request)
        else:
            muestra = lista_muestra[0]
            context = {'section': section, 'muestra': muestra}

            return render(request, 'muestras/detalle.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def reservar_muestra(request):
    """Desplegar y comprobar los valores a insertar.
           Historia de usuario: ALF-50 - Yo como Asistente de Laboratorio quiero poder ver el detalle de una muestra
           para conocer sus características.
           Se encarga de:
               * Reservar la muestra
        :param request: El HttpRequest que se va a responder.
        :type request: HttpRequest.
        :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a la listado
        de muestras. Sino redirecciona al mismo formulario mostrando los errores.
       """
    mensaje = ""
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = MuestraForm(request.POST or None, request.FILES or None)

            if form.is_valid():
                form.save()
                return redirect(reverse('home'))
            else:
                mensaje = 'Los datos ingresados para reservar la muestra no son correctos.'
        else:
            form = MuestraForm()

        return render(request, 'muestra/detalle.html', {'form': form, 'mensaje': mensaje})
    else:
        return HttpResponse('No autorizado', status = 401)


def reservar_maquina(request, pk):
    """Desplegar y comprobar los valores a consultar.
                Historia de usuario:     ALF-3 - Yo como Asistente de Laboratorio quiero poder ver la agenda de una
                máquina para visualizar cuándo podré usarla.
                Se encarga de:
                * Reservar una máquina en una fecha determinada.
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :param pk: La llave primaria de la máquina
            :type pk: String.
            :returns: HttpResponse -- La respuesta a la petición, con información del calendario para reservar la
                                      máquina.
        """
    if request.user.is_authenticated() and request.user.has_perm('LabModule.can_requestMachine'):
        lista_maquina = MaquinaEnLab.objects.filter(idMaquina_id = pk)
        if lista_maquina is None:
            # cambiar por listado de maquinas
            return lugar_list(request)
        else:
            maquina_en_lab = lista_maquina[0]
            maquina_profile = maquina_en_lab.idMaquina
            context = {'maquina_en_lab': maquina_en_lab, 'maquina_profile': maquina_profile}

            return render(request, 'maquinas/agenda.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def muestra_list(request):
    """Listar y filtrar muestras
               Historia de usuario:     ALF-52 - Yo como Asistente de Laboratorio quiero poder filtrar las muestras existentes por nombre para visualizar sólo las que me interesan.
               Se encarga de:
               * Listar, páginar y filtrar muestras
           :param request: El HttpRequest que se va a responder.
           :type request: HttpRequest.
           :returns: HttpResponse -- La respuesta a la petición, con un datatable con las muestras.
           Si el usuario no puede editarlas solo se muestran las muestras activas
       """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_listSample"):
        section = {}
        section['title'] = 'Listar Muestras'
        edita = request.user.has_perm("LabModule.can_editSample")
        if not edita:
            lista_muetras = Muestra.objects.all().filter(activa = True).extra(order_by = ['nombre'])
        else:
            lista_muetras = Muestra.objects.all().extra(order_by = ['nombre'])

        context = {'lista_muetras': lista_muetras, 'section': section}
        return render(request, 'muestras/listar.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


@csrf_exempt
def cargar_experimentos(request):
    """Realiza el cargue de datos de experimentos existentes por identificador del proyecto
                Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una
                franja de tiempo especifica para hacer uso de ella
                Se encarga de:
                    * Cargue de datos de experimentos
                :param request: El HttpRequest que se va a responder.
                :type request: HttpRequest.
                :returns: HttpResponse -- La información de experimentos existentes por identificador del proyecto
            """
    if request.GET['project_id'] != "":
        experiments = Experimento.objects.filter(projecto = request.GET['project_id'])
        experiments_dict = dict([(c.id, c.nombre) for c in experiments])
        return HttpResponse(json.dumps(experiments_dict))
    else:
        return HttpResponse()


@csrf_exempt
def cargar_protocolos(request):
    """Realiza el cargue de datos de protocolos existentes por identificador del experimento
                  Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una
                  franja de tiempo especifica para hacer uso de ella
                  Se encarga de:
                      * Cargue de datos de protocolos
                  :param request: El HttpRequest que se va a responder.
                  :type request: HttpRequest.
                  :returns: HttpResponse -- La información de protocolos existentes por identificador del experimento
              """
    if request.GET['experiment_id'] != "":
        protocols = Protocolo.objects.filter(experimento = request.GET['experiment_id'])
        protocols_dict = dict([(c.id, c.nombre) for c in protocols])
        return HttpResponse(json.dumps(protocols_dict))
    else:
        return HttpResponse()


@csrf_exempt
def cargar_pasos(request):
    """Realiza el cargue de datos de pasos existentes por identificador del protocolo
                    Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en
                    una franja de tiempo especifica para hacer uso de ella
                    Se encarga de:
                        * Cargue de datos de pasos
                    :param request: El HttpRequest que se va a responder.
                    :type request: HttpRequest.
                    :returns: HttpResponse -- La información de pasos existentes por identificador del protocolo
                """
    if request.GET['protocol_id'] != "":
        steps = Paso.objects.filter(protocolo = request.GET['protocol_id'])
        steps_dict = dict([(c.id, c.nombre) for c in steps])
        return HttpResponse(json.dumps(steps_dict))
    else:
        return HttpResponse()


def listar_solicitud_muestra(request):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_manageRequest"):
        section = {}
        section['title'] = 'Listar Solicitudes de Muestras'

        lista_solicitudes = Solicitud.objects.all().exclude(estado = 'aprobada')

        idSolicitudes = [solicitud.id for solicitud in lista_solicitudes]
        lista_MuestraSol = MuestraSolicitud.objects.all().filter(solicitud__in = idSolicitudes)

        context = {'section': section, 'solicitudes': lista_MuestraSol, 'mensaje': 'ok'}
        return render(request, 'solicitudes/aprobarMuestras.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def aprobar_solicitud_muestra(request):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_manageRequest"):
        section = {}
        section['title'] = 'Detalle Solicitud de Muestras'
        try:
            lista_lugares_pos = {}
            solicitud = Solicitud.objects.get(id = request.GET.get('pk', 0))
            muestraSolicitud = MuestraSolicitud.objects.get(solicitud = solicitud)
            usuario = Usuario.objects.get(user = request.user)
            contador = muestraSolicitud.cantidad
            muestra = muestraSolicitud.muestra
            if muestra.calc_disp() == 'Si':
                bandejas = Bandeja.objects.all().filter(muestra = muestra).extra(order_by = ['lugarAlmacenamiento'])
                for bandeja in bandejas:
                    if contador > 0 and bandeja.libre == False:
                        lugar = bandeja.lugarAlmacenamiento.nombre
                        if lugar in lista_lugares_pos:
                            lista_lugares_pos[lugar] += ',' + str(bandeja.posicion)
                        else:
                            lista_lugares_pos[lugar] = str(bandeja.posicion)
                        bandeja.libre = True
                        bandeja.save()
                        contador = contador - 1
                muestraSolicitud.solicitud.aprobador = usuario
                muestraSolicitud.solicitud.estado = 'aprobada'
                muestraSolicitud.solicitud.save()

                contexto = {'lugaresConPos'   : lista_lugares_pos, 'section': section,
                            'muestraSolicitud': muestraSolicitud}
                return render(request, 'solicitudes/resumenAprobadoMuestra.html', contexto)
            else:
                contexto = {
                    'mensaje': 'No es posible aprobar la solicitud porque no hay bandejas disponibles para suplir la demanda'}
        except ObjectDoesNotExist as e:
            contexto = {'mensaje': 'No hay solicitudes con el id solicitado'}
        except MultipleObjectsReturned as e:
            contexto = {'mensaje': 'Muchas solicitudes con ese id'}
        return render(request, 'solicitudes/aprobarMuestras.html', contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


@csrf_exempt
def maquina_reservations(request, pk):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_listRequest"):
        lista_maquina = MaquinaProfile.objects.filter(idSistema = pk)
        solicitudes = MaquinaSolicitud.objects.filter(maquina = lista_maquina)
        results = [ob.as_json(request.user.id) for ob in solicitudes]
        return HttpResponse(json.dumps(results), content_type = "application/json")
    else:
        return HttpResponse()
