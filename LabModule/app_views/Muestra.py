# -*- coding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from LabModule.app_forms.Muestra import MuestraSolicitudForm
from LabModule.app_forms.Solicitud import SolicitudForm
from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.MuestraEnBandeja import MuestraEnBandeja
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMuestra import SolicitudMuestra
from LabModule.app_models.Usuario import Usuario


def muestra_detail(request, pk, template_name = 'muestras/detalle.html'):
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
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewSample"):
        section = {'title': 'Ver Detalle'}

        inst_muestra = Muestra.objects.filter(id = pk)

        if inst_muestra is None:
            return muestra_list(request)
        else:
            muestra = inst_muestra[0]

            cant_muestras = MuestraEnBandeja.objects\
                .defer('id_bandeja', 'posX', 'posY').all()\
                .values('idMuestra')\
                .filter(idMuestra = muestra)\
                .annotate(cant_muestras = Count('idMuestra'))

        context = {'section'      : section,
                   'muestra'      : muestra,
                   'cant_muestras': cant_muestras[0]['cant_muestras']}

        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status = 401)


def muestra_list(request, template_name = 'muestras/listar.html'):
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
        section = {'title': 'Listar Muestras'}
        can_editSample = request.user.has_perm("LabModule.can_editSample")
        if not can_editSample:
            lista_muestras = Muestra.objects.all().filter(activa = True)
        else:
            lista_muestras = Muestra.objects.all()

        id_muestra = [muestra.id for muestra in lista_muestras]
        cant_muestras = MuestraEnBandeja.objects\
            .defer('id_bandeja', 'posX', 'posY').all()\
            .values('idMuestra')\
            .filter(idMuestra__in = id_muestra)\
            .annotate(cant_muestras = Count('idMuestra'))

        muestras_con_cantidad = zip(lista_muestras, cant_muestras)

        context = {'section'              : section,
                   'muestras_con_cantidad': muestras_con_cantidad}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status = 401)


def muestra_request(request, pk, template_name = 'muestras/solicitar.html'):
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
        section = {'title': 'Solicitar Muestra'}
        try:

            inst_muestra = Muestra.objects.filter(id = pk)
            inst_profile = Usuario.objects.get(user_id = request.user.id)

            list_proyectos = Proyecto.objects.filter(asistentes = inst_profile.id,
                                                     activo = True)
            if inst_muestra is None:
                return muestra_list(request)
            else:
                muestra = inst_muestra[0]

            form = SolicitudForm()
            form_muestra = MuestraSolicitudForm()
            cant_muestras = MuestraEnBandeja.objects\
                .defer('id_bandeja', 'posX', 'posY').all()\
                .values('idMuestra')\
                .filter(idMuestra = muestra)\
                .annotate(cant_muestras = Count('idMuestra'))

            if request.method == 'POST':

                requestObj = Solicitud()
                requestObj.descripcion = 'Solicitud de Muestra'
                requestObj.fechaInicial = request.POST['fechaInicial']
                requestObj.estado = 'creada'
                requestObj.solicitante = inst_profile
                requestObj.paso = Paso.objects.get(id = request.POST['step'])
                requestObj.save()

                sampleRequest = SolicitudMuestra()
                sampleRequest.solicitud = requestObj
                sampleRequest.muestra = muestra
                sampleRequest.cantidad = request.POST['cantidad']
                sampleRequest.tipo = 'uso'
                sampleRequest.save()

                return redirect(reverse('muestra-detail', kwargs = {'pk': pk}))

            contexto = {'section'      : section,
                        'form'         : form,
                        'form_muestra' : form_muestra,
                        'muestra'      : muestra,
                        'cant_muestras': cant_muestras[0]['cant_muestras'],
                        'proyectos'    : list_proyectos
                        }
        except ObjectDoesNotExist as e:
            print(e.message)
            contexto = {'mensaje': 'No hay proyectos asociados al usuario'}

        except MultipleObjectsReturned as e:
            print(e.message)
            contexto = {'mensaje': 'Muchas muestras con ese id'}

        return render(request, template_name, contexto)
    else:
        return HttpResponse('No autorizado', status = 401)
