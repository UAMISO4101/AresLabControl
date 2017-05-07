# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from AresLabControl.settings import BASE_DIR, EMAIL_HOST_USER
from LabModule.app_forms.Muestra import MuestraForm
from LabModule.app_forms.Muestra import MuestraSolicitudForm
from LabModule.app_forms.Solicitud import SolicitudForm
from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMuestra import SolicitudMuestra
from LabModule.app_models.Usuario import Usuario
from LabModule.app_utils.notificaciones import enviar_correo
from django.contrib.auth.models import User
import os


def notificacion_solicitud_muestra(request, muestra_nombre, solicitud_id):
    """Realiza la notificación de solicitud de muestras para el usuario que la necesita
               Historia de usuario: ALF-80:Yo como Asistente de Laboratorio quiero ser notificado vía correo
               electrónico si se aprobó o rechazo mi solicitud de muestra para saber si puedo hacer uso de la muestra
               Se encarga de:
                   * Comprobar si hay un usuario logueado
                   * Comprobar si el usuario tiene permisos para realizar la solicitud de muestras
                   * Realizar la solicitud de muestras
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :param muestra_nombre: Muesra a solicitar
            :type muestra: Muestra.
            :param solicitud_id: Id de la solicitud de la muestra.
            :type id: Identificador.
       """
    jefes_lab = User.objects.filter(groups__name='Jefe de Laboratorio')
    asunto = 'Envío de solicitud de muestra'
    usuario = Usuario.objects.get(nombre_usuario=request.user.username)
    to = [request.user.email]
    context = {'asistente': usuario.nombre_completo(),
               'muestra_nombre': muestra_nombre,
               'solicitud_id': solicitud_id}
    template_path = os.path.join(BASE_DIR, 'templates', 'correos', 'solicitud_muestra_asistente.txt')
    # Enviar correo al asistente
    enviar_correo(asunto, EMAIL_HOST_USER, to, template_path, '', context)
    # Enviar correo a los jefes
    if jefes_lab.exists():
        context = {'asistente': usuario.nombre_completo(),
                   'muestra_nombre': muestra_nombre,
                   'solicitud_id': solicitud_id}
        template_path = os.path.join(BASE_DIR, 'templates', 'correos', 'solicitud_muestra_jefe.txt')
        to = []
        for jefe in jefes_lab:
            to.append(jefe.email)
        enviar_correo(asunto, EMAIL_HOST_USER, to, template_path, '', context)


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

            muestra = Muestra.objects.get(id=request.GET.get('id', 0), activa=True)
            profile = Usuario.objects.get(user_id=request.user.id)
            proyectos = Proyecto.objects.filter(asistentes=profile.id, activo=True);

            if request.method == 'POST':

                requestObj = Solicitud()
                requestObj.descripcion = 'Solicitud de uso de muestra'
                requestObj.fechaInicial = request.POST['fechaInicial']
                requestObj.estado = 'creada'
                requestObj.solicitante = profile
                requestObj.paso = Paso.objects.get(id=request.POST['step'])
                requestObj.save()
                sampleRequest = SolicitudMuestra()
                sampleRequest.solicitud = requestObj
                sampleRequest.muestra = muestra
                sampleRequest.cantidad = request.POST['cantidad']
                sampleRequest.tipo = 'uso'
                sampleRequest.save()
                # Envío de notificación
                notificacion_solicitud_muestra(request, muestra.nombre, sampleRequest.id)
                return redirect(reverse('muestra-list', kwargs={}))

            else:
                form = SolicitudForm()
                form_muestra = MuestraSolicitudForm()
            contexto = {'form': form, 'mensaje': mensaje, 'muestra': muestra, 'proyectos': proyectos,
                        'form_muestra': form_muestra}
        except ObjectDoesNotExist as e:
            print(e.message)
            contexto = {'mensaje': 'No hay muestras o pasos con el id solicitado'}

        except MultipleObjectsReturned as e:
            print(e.message)
            contexto = {'mensaje': 'Muchas muestras con ese id'}

        return render(request, "solicitudes/crear_muestra_solicitud.html", contexto)
    else:
        return HttpResponse('No autorizado', status=401)


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
        lista_muestra = Muestra.objects.filter(id=pk)
        if lista_muestra is None:
            return muestra_list(request)
        else:
            muestra = lista_muestra[0]
            context = {'section': section, 'muestra': muestra}

            return render(request, 'muestras/detalle.html', context)
    else:
        return HttpResponse('No autorizado', status=401)


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
        return HttpResponse('No autorizado', status=401)


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
            lista_muetras = Muestra.objects.all().filter(activa=True).extra(order_by=['nombre'])
        else:
            lista_muetras = Muestra.objects.all().extra(order_by=['nombre'])

        context = {'lista_muetras': lista_muetras, 'section': section}
        return render(request, 'muestras/listar.html', context)
    else:
        return HttpResponse('No autorizado', status=401)
