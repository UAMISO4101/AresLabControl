# -*- coding: utf-8 -*-
import os
import json
import copy
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages

from AresLabControl.settings import BASE_DIR, EMAIL_HOST_USER
from LabModule.app_forms.Muestra import MuestraSolicitudForm
from LabModule.app_forms.Muestra import MuestraAddForm

from LabModule.app_forms.Solicitud import SolicitudForm
from LabModule.app_models.Muestra import Muestra
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMuestra import SolicitudMuestra
from LabModule.app_models.Usuario import Usuario
from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.MuestraEnBandeja import MuestraEnBandeja
from LabModule.app_models.MuebleEnLab import MuebleEnLab


from LabModule.app_utils.cursores import *
from LabModule.app_utils.notificaciones import enviar_correo


def notificacion_solicitud_muestra(request, muestra_nombre, solicitud_id):
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
    jefes_lab = User.objects.filter(groups__name = 'Jefe de Laboratorio')
    asunto = 'Envío de solicitud de muestra'
    usuario = Usuario.objects.get(nombre_usuario = request.user.username)
    to = [request.user.email]
    context = {'asistente'     : usuario.nombre_completo(),
               'muestra_nombre': muestra_nombre,
               'solicitud_id'  : solicitud_id}
    template_path = os.path.join(BASE_DIR, 'templates', 'correos', 'solicitud_muestra_asistente.txt')
    # Enviar correo al asistente
    enviar_correo(asunto, EMAIL_HOST_USER, to, template_path, '', context)
    # Enviar correo a los jefes
    if jefes_lab.exists():
        template_path = os.path.join(BASE_DIR, 'templates', 'correos', 'solicitud_muestra_jefe.txt')
        to = []
        for jefe in jefes_lab:
            to.append(jefe.email)
        enviar_correo(asunto, EMAIL_HOST_USER, to, template_path, '', context)


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

            inst_muestra = Muestra.objects.get(id = pk)
            inst_profile = Usuario.objects.get(user_id = request.user.id)

            list_proyectos = Proyecto.objects.filter(asistentes = inst_profile.id,
                                                     activo = True)
            if inst_muestra is None:
                return muestra_list(request)
            else:
                muestra = inst_muestra
                detalle_completo = obtenerBandejasMuestras(str(muestra.id))

            form = SolicitudForm()
            form_muestra = MuestraSolicitudForm()

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

                # Envío de notificación
                notificacion_solicitud_muestra(request, muestra.nombre, sampleRequest.id)

                return redirect(reverse('muestra-detail', kwargs = {'pk': pk}))

            contexto = {'section'         : section,
                        'form'            : form,
                        'form_muestra'    : form_muestra,
                        'muestra'         : muestra,
                        'detalle_completo': detalle_completo,
                        'proyectos'       : list_proyectos
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


def muestra_detail(request, pk, template_name = 'muestras/detalle.html'):
    """Desplegar y comprobar los valores a consultar.
                Historia de usuario: ALF-50 - Yo como Asistente de Laboratorio quiero poder ver el detalle de una
                muestra para conocer sus características.
                Se encarga de:
                * Mostar el formulario para consultar las muestras.
            :param request: El HttpRequest que se va a responder.cls
            :type request: HttpRequest.
            :param pk: La llave primaria de la muestra
            :type pk: String.
            :returns: HttpResponse -- La respuesta a la petición, con información de la muestra existente.
        """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewSample"):
        section = {'title': 'Ver Detalle'}

        inst_muestra = Muestra.objects.get(id = pk)

        if inst_muestra is None:
            return muestra_list(request)
        else:
            muestra = inst_muestra
            detalle_completo = obtenerBandejasMuestras(str(muestra.id))

        context = {'section'         : section,
                   'muestra'         : muestra,
                   'detalle_completo': detalle_completo}

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
        detalle_completo = obtenerListadoMuestras(can_editSample)

        context = {'section'         : section,
                   'detalle_completo': detalle_completo}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status = 401)


def muestra_position(request,pk,template_name='muestras/agregar.html'):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addSample"):
        section='Guardar muestra'
        muestra=get_object_or_404(Muestra,pk=pk)
        form=MuestraAddForm(request.POST or None,maximo=disponibilidad_muestra(muestra))
        if request.POST and form.is_valid():
            cantidad=form.cleaned_data['cantidad']
            rta,total=agregar_cantidad(muestra,cantidad)
            section="Confirmar ubicación "
            context = {'section': section,'muestra':muestra,'detalle_completo':rta}
            seriali=[]
            for bdg in rta:
                ag={}
                ag['bandeja']=bdg['bandeja'].id
                ag['posX']=bdg['posX']
                ag['posY']=bdg['posY']
                seriali.append(ag)
            request.session['a_aprobar'] = seriali
            return render(request,'muestras/detalle_guardado.html',context)
        context = {'section': section,'form':form,'muestra':muestra}
        return render(request, template_name, context)
    return HttpResponse('No autorizado', status = 401)

def muestra_save(request,pk):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addSample"):
        a_aprobar = request.session.get('a_aprobar')
        creadas=copy.copy(a_aprobar)
        muestra2=Muestra.objects.get(id=pk)
        for muestra in a_aprobar:
            try:
                bandeja=Bandeja.objects.get(id=muestra['bandeja'])
                x=muestra['posX']
                y=muestra['posY']
                creada,existia=MuestraEnBandeja.objects.get_or_create(idMuestra=muestra2,idBandeja=bandeja,posX=x,posY=y)
                if existia:
                    creadas.remove(muestra)
                else:
                    print(creada)
            except Exception as e:
                 print(str(e))
        if not len(creadas)==0:
            messages.error(request, 'Algunas de las muestras no pudieron ser guardadas'+str(len(creadas)),extra_tags='alert-danger')
        else:
            messages.success(request,'Las muestras se han agregado exitosamente')
        return redirect(reverse('muestra-detail', kwargs = {'pk': pk}))
       
            


def disponibilidad_muestra(muestra):
    almacenamiento=muestra.alamacenamientos.all()
    total=0
    for alm in almacenamiento:
        total+=alm.get_max_capacidad()
        bandejas =Bandeja.getBandejas(alm)
        for bandeja in bandejas:
            muestras=MuestraEnBandeja.getPosiciones(bandeja)
            for muestra in muestras:
                total+=-1
    return total
def agregar_cantidad(muestra,cantidad):
    almacenamiento=muestra.alamacenamientos.all().order_by('idSistema')
    alamcenamientosArr=[]
    total=0
    for alm in almacenamiento:
        bandejas =Bandeja.getBandejas(alm)
        maximo=alm.numX*alm.numY
        muebleEnLab=MuebleEnLab.objects.get(idMueble=alm.mueble)
        for bandeja in bandejas:
            gradillasOcupadas=MuestraEnBandeja.getPosiciones(bandeja)
            cant=maximo-gradillasOcupadas.count()
            if cant>0:
                matriz=[[0 for x in range(alm.numX)] for y in range(alm.numY)]
                for gradilla in gradillasOcupadas:
                    matriz[gradilla.posY-1][gradilla.posX-1]=1
                for  y in range(alm.numY):
                    for x in range(alm.numX):
                        if matriz[y][x]==0 and total<cantidad:
                            detalle={}
                            detalle['muebleEnLab']=muebleEnLab
                            detalle['alma']=alm
                            detalle['bandeja']=bandeja
                            detalle['posX']=x+1
                            detalle['posY']=y+1
                            alamcenamientosArr.append(detalle)
                            total+=1
            if total==cantidad:
                break
        

        if total==cantidad:
            break
    return alamcenamientosArr,total
def obtenerBandejasMuestras(muestraId):
    "Obtiene la lista que va a poblar la grilla de presentacion del resumen de la solicitud"

    query = queryBandejasMuestras + 'WHERE mb."idMuestra_id" = ' + muestraId
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
    return rows


def obtenerListadoMuestras(can_editSample):
    if not can_editSample:
        query = queryListaMuestrasAll
    else:
        query = queryListaMuestras

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
    return rows

