# -*- coding: utf-8 -*-
import json
import os

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from AresLabControl.settings import BASE_DIR, EMAIL_HOST_USER
from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMaquina import SolicitudMaquina
from LabModule.app_models.SolicitudMuestra import SolicitudMuestra
from LabModule.app_models.Usuario import Usuario
from LabModule.app_utils.notificaciones import enviar_correo


def solicitud_muestra_list(request, template_name = 'solicitudes/muestras/listar.html'):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_listRequest"):
        section = {'title': 'Listar Solicitudes de Muestras'}

        lista_solicitudes = Solicitud.objects.all().exclude(estado = 'aprobada')

        id_solicitudes = [solicitud.id for solicitud in lista_solicitudes]
        lista__muestra_sol = SolicitudMuestra.objects.all().filter(solicitud__in = id_solicitudes)

        context = {'section'    : section,
                   'solicitudes': lista__muestra_sol}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status = 401)


def solicitud_muestra_aprobar(request, pk, template_name = 'solicitudes/muestras/detalle.html'):
    section = {'title': 'Aprobar Solicitud de Muestras', 'aprobar': True}
    return solicitud_muestra_detail(request, pk, template_name, section)


def solicitud_muestra_rechazar(request, pk, template_name = 'solicitudes/muestras/detalle.html'):
    section = {'title': 'Rechazar Solicitud de Muestras', 'aprobar': False}
    return solicitud_muestra_detail(request, pk, template_name, section)


def solicitud_muestra_detail(request, pk, template_name = 'solicitudes/muestras/detalle.html', section = None):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_manageRequest"):
        if section is None:
            mysection = {'title': 'Detalle Solicitud de Muestras', 'aprobar': None}
        else:
            mysection = section

        solicitud = Solicitud.objects.filter(id = pk)
        solicitud_muestra = SolicitudMuestra.objects.get(solicitud = solicitud)
        approver_user = Usuario.objects.get(user = request.user)

        solicitud_muestra.solicitud.aprobador = approver_user

        if request.method == 'POST':
            return post_solicitud_muestra(solicitud_muestra, mysection)

        contexto = {'section'          : mysection,
                    'solicitud_muestra': solicitud_muestra}
        return render(request, template_name, contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


def post_solicitud_muestra(solicitud_muestra, section):
    if section.get('aprobar'):
        solicitud_muestra.solicitud.estado = 'aprobada'
    else:
        solicitud_muestra.solicitud.estado = 'rechazada'

    solicitud_muestra.solicitud.save()
    solicitud_muestra.save()

    # Enviar notificación a asistente de laboratorio
    solicitante_nombre = solicitud_muestra.solicitud.solicitante.nombre_completo()
    solicitante_email = solicitud_muestra.solicitud.solicitante.correo_electronico
    muestra_nombre = solicitud_muestra.muestra.nombre
    solicitud_id = solicitud_muestra.solicitud.id
    jefe = solicitud_muestra.solicitud.aprobador.nombre_completo()

    solicitud_muestra_notificacion(jefe,
                                   solicitante_nombre,
                                   solicitante_email,
                                   muestra_nombre,
                                   solicitud_id)

    return redirect('solicitud-muestra-list')


def solicitud_muestra_notificacion(jefe, solicitante_nombre, solicitante_email, muestra_nombre, solicitud_id):
    """Realiza la notificación de solicitud de muestras para el usuario que la necesita
               Historia de usuario: ALF-80:Yo como Asistente de Laboratorio quiero ser notificado vía correo
               electrónico si se aprobó o rechazo mi solicitud de muestra para saber si puedo hacer uso de la muestra
               Se encarga de:
                   * Realiza la notificación de la solicitud de muestras
            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :param muestra_nombre: Muesra a solicitar
            :type muestra: Muestra.
            :param solicitud_id: Id de la solicitud de la muestra.
            :type id: Identificador.
       """
    asunto = 'Aprobación de la solicitud de la muestra'
    to = [solicitante_email]
    context = {'asistente'     : solicitante_nombre,
               'jefe'          : jefe,
               'muestra_nombre': muestra_nombre,
               'solicitud_id'  : solicitud_id}
    template_path = os.path.join(BASE_DIR, 'templates', 'correos', 'solicitud_muestra_asistente_aprobacion.txt')
    # Enviar correo al asistente
    enviar_correo(asunto, EMAIL_HOST_USER, to, template_path, '', context)


@csrf_exempt
def maquina_reservations(request, pk):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_listRequest"):
        lista_maquina = Maquina.objects.filter(idSistema = pk)
        solicitudes = SolicitudMaquina.objects.filter(maquina = lista_maquina)
        results = [ob.as_json(request.user.id) for ob in solicitudes]
        return HttpResponse(json.dumps(results), content_type = "application/json")
    else:
        return HttpResponse()


def solicitud_maquina_list(request, template_name = 'solicitudes/maquinas/listar.html'):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_manageRequest"):
        section = {'title': 'Listar Solicitudes de Máquinas'}

        lista_solicitudes = Solicitud.objects.all().exclude(estado = 'aprobada')

        idSolicitudes = [solicitud.id for solicitud in lista_solicitudes]
        lista_MaquinaSol = SolicitudMaquina.objects.all().filter(solicitud__in = idSolicitudes)

        context = {'section'    : section,
                   'solicitudes': lista_MaquinaSol,
                   'mensaje'    : 'ok'}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status = 401)


def solicitud_maquina_aprobar(request, pk, template_name = 'solicitudes/maquinas/detalle.html'):
    section = {'title': 'Aprobar Solicitud de Máquinas', 'aprobar': True}
    return solicitud_maquina_detail(request, pk, template_name, section)


def solicitud_maquina_rechazar(request, pk, template_name = 'solicitudes/maquinas/detalle.html'):
    section = {'title': 'Rechazar Solicitud de Máquinas', 'aprobar': False}
    return solicitud_maquina_detail(request, pk, template_name, section)


def solicitud_maquina_detail(request, pk, template_name = 'solicitudes/maquinas/detalle.html', section = None):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_manageRequest"):
        if section is None:
            mysection = {'title': 'Detalle Solicitud de Máquinas', 'aprobar': None}
        else:
            mysection = section

        solicitud = Solicitud.objects.filter(id = pk)
        solicitud_maquina = SolicitudMaquina.objects.get(solicitud = solicitud)
        approver_user = Usuario.objects.get(user = request.user)

        solicitud_maquina.solicitud.aprobador = approver_user

        if request.method == 'POST':
            return post_solicitud_maquina(solicitud_maquina, mysection)

        contexto = {'section'          : mysection,
                    'solicitud_maquina': solicitud_maquina}
        return render(request, template_name, contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


def post_solicitud_maquina(solicitud_maquina, section):
    if section.get('aprobar'):
        solicitud_maquina.solicitud.estado = 'aprobada'
    else:
        solicitud_maquina.solicitud.estado = 'rechazada'

    solicitud_maquina.solicitud.save()
    solicitud_maquina.save()

    # Enviar notificación a asistente de laboratorio
    solicitante_nombre = solicitud_maquina.solicitud.solicitante.nombre_completo()
    solicitante_email = solicitud_maquina.solicitud.solicitante.correo_electronico
    muestra_nombre = solicitud_maquina.maquina.mueble.nombre
    solicitud_id = solicitud_maquina.solicitud.solicitud_id
    jefe = solicitud_maquina.solicitud.aprobador.nombre_completo()

    solicitud_muestra_notificacion(jefe,
                                   solicitante_nombre,
                                   solicitante_email,
                                   muestra_nombre,
                                   solicitud_id)

    return redirect('solicitud-muestra-detail')
