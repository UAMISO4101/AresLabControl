import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMaquina import SolicitudMaquina
from LabModule.app_models.SolicitudMuestra import SolicitudMuestra
from LabModule.app_models.Usuario import Usuario


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


def solicitud_muestra_negar(request, pk, template_name = 'solicitudes/muestras/detalle.html'):
    section = {'title': 'Negar Solicitud de Muestras', 'aprobar': False}
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
            return comprobar_post_solicitud(solicitud_muestra, mysection)

        contexto = {'section'          : mysection,
                    'solicitud_muestra': solicitud_muestra}
        return render(request, template_name, contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


@csrf_exempt
def maquina_reservations(request, pk):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_listRequest"):
        lista_maquina = Maquina.objects.filter(idSistema = pk)
        solicitudes = SolicitudMaquina.objects.filter(maquina = lista_maquina)
        results = [ob.as_json(request.user.id) for ob in solicitudes]
        return HttpResponse(json.dumps(results), content_type = "application/json")
    else:
        return HttpResponse()


def comprobar_post_solicitud(solicitud_muestra, section):
    if section.get('aprobar'):
        solicitud_muestra.solicitud.estado = 'aprobada'
    else:
        solicitud_muestra.solicitud.estado = 'rechazada'
    solicitud_muestra.save()
    return redirect('solicitud-muestra-detail')
