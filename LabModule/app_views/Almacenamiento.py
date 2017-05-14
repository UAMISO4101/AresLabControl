# -*- coding: utf-8 -*-
from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from LabModule.app_forms.Almacenamiento import AlmacenamientoForm
from LabModule.app_forms.Mueble import MuebleForm
from LabModule.app_forms.Mueble import PosicionesMuebleForm
from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.MuebleEnLab import MuebleEnLab
from LabModule.app_models.MuestraEnBandeja import MuestraEnBandeja


def lugar_add(request, template_name='almacenamientos/agregar.html'):
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
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addStorage"):
        section = {'title': 'Agregar Almacenamiento', 'agregar': True}
        mensaje = ""
        form = MuebleForm(request.POST or None, request.FILES or None)
        formAlmacenamiento = AlmacenamientoForm(request.POST or None, request.FILES or None)
        formPos = PosicionesMuebleForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            return comprobarPostLugar(form, formAlmacenamiento, formPos, request, template_name, section)
        context = {'form': form,
                   'formAlmacenamiento': formAlmacenamiento,
                   'formPos': formPos,
                   'mensaje': mensaje,
                   'section': section}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status=401)


def lugar_detail(request, pk, template_name='almacenamientos/detalle.html'):
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
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewSample"):
        section = {'title': 'Ver Detalle ', 'agregar': "ver"}

        lugar = get_object_or_404(Almacenamiento, pk=pk)
        mueble = lugar.mueble
        laboratorio = MuebleEnLab.get_laboratorio(mueble)

        bandejas = [bandeja.id for bandeja in Bandeja.objects.filter(almacenamiento=lugar)]
        espaciosOcupados = len([m for m in MuestraEnBandeja.objects.filter(idBandeja__in=bandejas)])
        espacioslibres = lugar.get_max_capacidad() - espaciosOcupados

        pos = MuebleEnLab.objects.get(idLaboratorio=laboratorio,
                                      idMueble=mueble)

        context = {'lugar': lugar,
                   'espaciosOcupados': espaciosOcupados,
                   'espacioslibres': espacioslibres,
                   'laboratorio': laboratorio,
                   'mueble': mueble,
                   'pos': pos,
                   'section': section}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status=401)


def lugar_update(request, pk, template_name='almacenamientos/agregar.html'):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_editStorage"):
        section = {'title': 'Modificar Lugar de Almacenamiento', 'agregar': False}

        inst_almacenamiento = get_object_or_404(Almacenamiento, pk=pk)
        inst_mueble = inst_almacenamiento.mueble
        inst_ubicacion = get_object_or_404(MuebleEnLab, idMueble=inst_mueble)

        form = MuebleForm(request.POST or None,
                          request.FILES or None,
                          instance=inst_mueble)
        formAlmacenamiento = AlmacenamientoForm(request.POST or None,
                                                request.FILES or None,
                                                instance=inst_almacenamiento)
        formPos = PosicionesMuebleForm(request.POST or None,
                                       request.FILES or None,
                                       instance=inst_ubicacion)

        return comprobarPostLugar(form, formAlmacenamiento, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status=401)


def lugar_list(request, template_name='almacenamientos/listar.html'):
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
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_listStorage"):
        section = {'title': 'Listar Almacenamientos'}
        can_editStorage = request.user.has_perm("LabModule.can_editStorage")
        lista_almacenamiento = obtener_lugares(not can_editStorage)

        context = {'section': section,
                   'lista_lugares': lista_almacenamiento}
        return render(request, template_name, context)
    else:
        return HttpResponse('No autorizado', status=401)


def comprobarPostLugar(form, formAlmacenamiento, formPos, request, template_name, section):
    mensaje = ""
    if form.is_valid() and formPos.is_valid() and formAlmacenamiento.is_valid():

        new_furniture = form.save(commit=False)
        new_furniture.tipo = 'almacenamiento'
        new_storage = formAlmacenamiento.save(commit=False)
        new_storage_loc = formPos.save(commit=False)

        idLaboratorio = formPos.cleaned_data['idLaboratorio']
        posX = formPos.cleaned_data['posX']
        posY = formPos.cleaned_data['posY']

        if section['agregar']:
            if not formPos.es_ubicacion_libre():
                messages.error(request, "El lugar en el que desea guadar ya esta ocupado", extra_tags="danger")
        elif not formPos.es_el_mismo_mueble(new_furniture.id,
                                            idLaboratorio,
                                            posX,
                                            posY):
            if not formPos.es_ubicacion_libre():
                messages.error(request, "El lugar en el que desea guadar ya esta ocupado", extra_tags="danger")
        if not formPos.es_ubicacion_rango():
            mensaje = "La posición [" + \
                      str(new_storage_loc.posX) + "," + \
                      str(new_storage_loc.posY) + "] no se encuentra en el rango del laboratorio"
            messages.error(request, mensaje, extra_tags="danger")
        else:
            new_furniture.save()
            new_storage.mueble = new_furniture
            new_storage.save()
            new_storage_loc.idMueble = new_furniture
            new_storage_loc.save()

        if section['agregar']:
            messages.success(request, "El lugar de almacenamiento se añadió exitosamente")
        else:
            messages.success(request, "El lugar de almacenamiento se actualizó correctamente")
        return redirect(reverse('lugar-detail', kwargs={'pk': new_storage.pk}))
    context = {'form': form,
               'formAlmacenamiento': formAlmacenamiento,
               'formPos': formPos,
               'mensaje': mensaje,
               'section': section,
               }
    return render(request, template_name, context)


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def obtener_lugares(cannot_editStorage):
    """
    Obtiene los lugares de almacenamiento para filtrarlos por protocolo
    :param cannot_editStorage: Indica si puede o no editar los registros de almacanamiento
    :return: listado de lugares de almacenamiento
    """
    query = '''SELECT DISTINCT "idSistema"
                       ,mue.nombre
                       ,initcap(lab."idLaboratorio") || ' ' || initcap(lab.nombre) || ':'
                       || muela."posX" || ',' || muela."posY" AS ubicacion
                       ,temperatura
                       ,pro.nombre AS protocolo
                       ,ba.posicion AS bandeja
                       ,mu.id AS id_muestra
	                   ,mu.nombre AS muestra
                   FROM "LabModule_almacenamiento" AS alm
                   LEFT JOIN "LabModule_bandeja" AS ba ON ba.almacenamiento_id = alm."idSistema"
                   LEFT JOIN "LabModule_muestraenbandeja" AS meb ON meb."idBandeja_id" = ba.id
                   LEFT JOIN "LabModule_muestra" AS mu ON mu.id = meb."idMuestra_id"
                   LEFT JOIN "LabModule_paso_muestras" AS pam ON pam."muestra_id" = mu.id
                   LEFT JOIN "LabModule_paso" AS pa ON pa.id = pam."paso_id"
                   LEFT JOIN "LabModule_protocolo" AS pro ON pro.id = pa."protocolo_id"
                   LEFT JOIN "LabModule_mueble" AS mue ON mue.id = alm."mueble_id"
                   LEFT JOIN "LabModule_muebleenlab" AS muela ON muela."idMueble_id" = mue."id"
                   LEFT JOIN "LabModule_laboratorio" AS lab ON lab."idLaboratorio" = muela."idLaboratorio_id"
                   WHERE mue.tipo = 'almacenamiento' '''

    if cannot_editStorage:
        query += ''' AND mue.estado = true '''

    query += ''' ORDER BY 2'''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
    return rows
