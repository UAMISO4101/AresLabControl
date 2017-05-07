# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from LabModule.app_forms.Almacenamiento import AlmacenamientoForm
from LabModule.app_forms.Mueble import MuebleForm
from LabModule.app_forms.Mueble import PosicionesMuebleForm
from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.AlmacenamientoEnLab import AlmacenamientoEnLab
from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.Laboratorio import Laboratorio


def lugar_add(request, template_name = 'almacenamientos/agregar.html'):
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
        form = MuebleForm()
        formAlmacenamiento=AlmacenamientoForm()
        formPos = PosicionesMuebleForm()
        if request.method == 'POST':
            form = MuebleForm(request.POST or None, request.FILES or None)
            formAlmacenamiento=AlmacenamientoForm(request.POST or None, request.FILES or None)
            formPos = PosicionesMuebleForm(request.POST or None, request.FILES or None)
            if form.is_valid() and formPos.is_valid() and formAlmacenamiento.is_valid():

                mueble = form.save(commit = False)
                almacenamiento=formAlmacenamiento.save(commit = False)
                muebleEnLab = formPos.save(commit = False)

                if not formPos.es_ubicacion_libre():
                    print("erros")
                    messages.error(request, "El lugar en el que desea guadar ya esta ocupado", extra_tags = "danger")
                elif not formPos.es_ubicacion_rango():
                    mensaje = "La posición [" + str(muebleEnLab.posX) + "," + str(
                            muebleEnLab.posY) + "] no se encuentra en el rango del laboratorio"
                    messages.error(request,mensaje, extra_tags = "danger")
                else:
                    mueble.save()
                    almacenamiento.mueble=mueble
                    almacenamiento.save()
                    muebleEnLab.idMueble=mueble
                    muebleEnLab.save()
                    pos=1
                    for cantidad in range(almacenamiento.numZ):
                        bandeja = Bandeja(almacenamiento = almacenamiento,posicion = pos)
                        bandeja.save()
                        pos+=1
                    messages.success(request, "El lugar se añadio exitosamente")
                    return HttpResponseRedirect(reverse('lugar-detail', kwargs = {'pk': almacenamiento.pk}))
        
        context = {'form': form, 'formAlmacenamiento':formAlmacenamiento,'formPos': formPos, 'mensaje': mensaje, 'section': section}
        print(form.errors,formAlmacenamiento.errors,formPos.errors)
        return render(request, 'almacenamientos/agregar.html', context)
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
            lista_almacenamiento = Almacenamiento.objects.all().filter(activa = True).extra(order_by = ['nombre'])
        else:
            lista_almacenamiento = Almacenamiento.objects.all().extra(order_by = ['nombre'])

        id_almacenamiento = [maquina.id for maquina in lista_almacenamiento]
        lista_Posiciones = AlmacenamientoEnLab.objects.all().filter(idLugar__in = id_almacenamiento)
        lugaresConUbicacion = zip(lista_almacenamiento, lista_Posiciones)
        context = {'section': section, 'lista_lugares': lugaresConUbicacion}
        return render(request, 'almacenamientos/listar.html', context)
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
        lista_lugar = AlmacenamientoEnLab.objects.filter(idLugar_id = pk)
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

            laboratorio = Laboratorio.objects.get(pk = lugar.idLaboratorio_id).nombre

            context = {'lugar'      : lugar, 'bandejasOcupadas': bandejasOcupadas, 'bandejasLibres': bandejasLibres,
                       'laboratorio': laboratorio}
            return render(request, 'almacenamientos/detalle.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def comprobarPostAlmacenamiento(form, formAlmacenamiento, formPos, request, template_name, section):
    if form.is_valid() and formPos.is_valid() and formAlmacenamiento.is_valid():
        mueble = form.save(commit = False)
        almacenamiento = formAlmacenamiento.save(commit = False)
        muebleEnLab = formPos.save(commit = False)

        if formPos.es_ubicacion_libre():
            messages.error(request, "El lugar en el que desea guadar ya esta ocupado", extra_tags = "danger")
        else:
            lab = muebleEnLab.idLaboratorio
            masX = lab.numX >= muebleEnLab.posX
            masY = lab.numY >= muebleEnLab.posY
            posible = masX and masY
            if not posible:
                if not masX:
                    formPos.add_error("posX", "La posición x sobrepasa el valor máximo de " + str(lab.numX))
                if not masY:
                    formPos.add_error("posY", "La posición y sobrepasa el valor máximo de " + str(lab.numY))
            else:
                if almacenamiento.numZ <= 0:
                    form.add_error("capacidad", "La capacidad debe ser mayor a cero")
                    messages.error(request, "La capacidad del lugar de almacenamiento debe ser mayor a cero",
                                   extra_tags = "danger")
                else:
                    mueble.save()
                    almacenamiento.mueble_id = mueble
                    almacenamiento.save()
                    muebleEnLab.idMueble = mueble
                    muebleEnLab.save()

                    for idBandeja in range(almacenamiento.numZ):
                        bandeja = Bandeja(lugarAlmacenamiento = mueble,
                                          posicion = idBandeja)
                        bandeja.save()
                    messages.success(request, "El lugar se añadio exitosamente")
                    return HttpResponseRedirect(reverse('lugar-detail', kwargs = {'pk': mueble.pk}))
    else:
        form = MuebleForm()
        formAlmacenamiento = AlmacenamientoForm()
        formPos = PosicionesMuebleForm()
    context = {'form'              : form,
               'formAlmacenamiento': formAlmacenamiento,
               'formPos'           : formPos,
               'section'           : section}
    return render(request, 'almacenamientos/agregar.html', context)
