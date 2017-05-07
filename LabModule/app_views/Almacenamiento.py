# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404

from LabModule.app_forms.Almacenamiento import AlmacenamientoForm
from LabModule.app_forms.Mueble import MuebleForm
from LabModule.app_forms.Mueble import PosicionesMuebleForm
from LabModule.app_models.Almacenamiento import Almacenamiento
from LabModule.app_models.Bandeja import Bandeja
from LabModule.app_models.Laboratorio import Laboratorio
from LabModule.app_models.Mueble import Mueble
from LabModule.app_models.MuebleEnLab import MuebleEnLab
from LabModule.app_models.MuestraEnBandeja import MuestraEnBandeja


def lugar_add(request, template_name = 'almacenamientos/agregar.html',pk=None):
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
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addStorage"):
        form = MuebleForm(request.POST or None, request.FILES or None)
        formAlmacenamiento=AlmacenamientoForm(request.POST or None, request.FILES or None)
        formPos = PosicionesMuebleForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            form = MuebleForm(request.POST or None, request.FILES or None)
            formAlmacenamiento=AlmacenamientoForm(request.POST or None, request.FILES or None)
            formPos = PosicionesMuebleForm(request.POST or None, request.FILES or None)
            if form.is_valid() and formPos.is_valid() and formAlmacenamiento.is_valid():

                mueble = form.save(commit = False)
                mueble.tipo='almacenamiento'
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
            lista_almacenamiento = Mueble.objects.all().filter(estado = True,tipo='almacenamiento').extra(order_by = ['nombre'])
        else:
            lista_almacenamiento = Mueble.objects.all().filter(tipo='almacenamiento').extra(order_by = ['nombre'])
        
        id_almacenamiento = [lugar.id for lugar in lista_almacenamiento]
        lista_Posiciones = MuebleEnLab.objects.all().filter(idMueble__in = id_almacenamiento)
        lugares=Almacenamiento.objects.all().filter(mueble__in = id_almacenamiento)
        lugaresConUbicacion = zip(lista_almacenamiento, lista_Posiciones,lugares)
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
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewSample"):
        lugar=get_object_or_404(Almacenamiento, pk=pk)
        mueble=lugar.mueble    
        bandejas=[bandeja.id for bandeja in Bandeja.objects.filter(almacenamiento=lugar)]
        espaciosOcupados= len([m for m in MuestraEnBandeja.objects.filter(idBandeja__in=bandejas)])
        espacioslibres=lugar.get_max_capacidad()-espaciosOcupados
        laboratorio = MuebleEnLab.get_laboratorio(mueble)
        pos=MuebleEnLab.objects.get(idLaboratorio=laboratorio,idMueble=mueble)
        context = {'lugar'      : lugar, 'espaciosOcupados': espaciosOcupados, 'espacioslibres': espacioslibres,
                   'laboratorio': laboratorio,'mueble':mueble,'pos':pos}
        return render(request, 'almacenamientos/detalle.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)
def lugar_edit(request, pk):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addStorage"):
        section = {'title': 'Editar lugar de almacenamiento'}
        alamacenamiento=get_object_or_404(Almacenamiento, pk=pk)
        mueble=alamacenamiento.mueble
        muebleEnLab=MuebleEnLab.objects.get(idLaboratorio=MuebleEnLab.get_laboratorio(mueble),idMueble=mueble)
        form = MuebleForm(instance=mueble)
        formAlmacenamiento=AlmacenamientoForm(instance=alamacenamiento)
        formPos = PosicionesMuebleForm(instance=muebleEnLab)
        mueble = form.save(commit = False)
        mueble.tipo='almacenamiento'
        almacenamiento=formAlmacenamiento.save(commit = False)
        muebleEnLab = formPos.save(commit = False)
        
        if not formPos.es_ubicacion_libre() and not  formPos.es_el_mismo_mueble(mueble.id):
            print("erros")
            messages.error(request, "El lugar en el que desea guadar ya esta ocupado", extra_tags = "danger")
        elif not formPos.es_ubicacion_rango():
            mensaje = "La posición [" + str(muebleEnLab.posX) + "," + str(
                    muebleEnLab.posY) + "] no se encuentra en el rango del laboratorio"
            messages.error(request,mensaje, extra_tags = "danger")
        else:
            pinrt("llega")
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
            messages.success(request, "El lugar se modifico exitosamente")
            return HttpResponseRedirect(reverse('lugar-detail', kwargs = {'pk': almacenamiento.pk}))

    context = {'form': form, 'formAlmacenamiento':formAlmacenamiento,'formPos': formPos, 'section': section}
    print(form.errors,formAlmacenamiento.errors,formPos.errors)
    return render(request, 'almacenamientos/agregar.html', context)
