# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from LabModule.app_forms.Maquina import MaquinaForm
from LabModule.app_forms.Mueble import MuebleForm
from LabModule.app_forms.Mueble import PosicionesMuebleForm
from LabModule.app_forms.Solicitud import SolicitudForm
from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.MaquinaEnLab import MaquinaEnLab
from LabModule.app_models.Mueble import Mueble
from LabModule.app_models.MuebleEnLab import MuebleEnLab
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMaquina import SolicitudMaquina
from LabModule.app_models.Usuario import Usuario


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
    section = {'title': 'Agregar Máquina', 'agregar': True}
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addMachine"):
        form = MuebleForm(request.POST or None, request.FILES or None)
        formMaquina = MaquinaForm(request.POST or None, request.FILES or None)
        formPos = PosicionesMuebleForm(request.POST or None, request.FILES or None)
        return comprobarPostMaquina(form, formMaquina, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status = 401)


def maquina_detail(request, pk, template_name = 'maquinas/detalle.html'):
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewMachine"):
        maquina = get_object_or_404(Maquina, pk = pk)
        maquinaEnLab = get_object_or_404(MaquinaEnLab, idMaquina = maquina)
        mensaje = ""
        section = {'title': 'Ver Detalle ', 'agregar': "ver"}
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
        section = {'title': 'Modificar Máquina', 'agregar': False}

        inst_mueble = get_object_or_404(Mueble, pk = pk)
        ints_maquina = get_object_or_404(Maquina, pk = pk)
        inst_ubicacion = get_object_or_404(MuebleEnLab, idMaquina = inst_mueble)

        form = MuebleForm(request.POST or None, request.FILES or None, instance = inst_mueble)
        formMaquina = MaquinaForm(request.POST or None, request.FILES or None, instance = ints_maquina)
        formPos = PosicionesMuebleForm(request.POST or None, request.FILES or None, instance = inst_ubicacion)

        return comprobarPostMaquina(form, formMaquina, formPos, request, template_name, section)
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
            lista_maquinas = Maquina.objects.all().filter(activa = True).extra(order_by = ['nombre'])
        else:
            lista_maquinas = Maquina.objects.all().extra(order_by = ['nombre'])

        id_maquina = [maquina.idSistema for maquina in lista_maquinas]
        lista_Posiciones = MaquinaEnLab.objects.all().filter(idMaquina__in = id_maquina)
        maquinasConUbicacion = zip(lista_maquinas, lista_Posiciones)
        context = {'section': section, 'maquinasBien': maquinasConUbicacion}
        return render(request, 'maquinas/listar.html', context)
    else:
        return HttpResponse('No autorizado', status = 401)


def maquina_request(request):
    """Realiza la solicitud de máquinas por el usuario que la necesita
        Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una Maquina normal en una
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
        try:
            maquina = Maquina.objects.get(pk = request.GET.get('idAlmacenamiento', 0), activa = True)
            profile = Usuario.objects.get(user_id = request.user.id)
            maquinaEnLab = MaquinaEnLab.objects.get(idMaquina = maquina.pk)
            proyectos = Proyecto.objects.filter(asistentes = profile.id, activo = True)
            form = SolicitudForm()
            if request.method == 'POST':
                if form.verificar_fecha(maquina.pk, request.POST['fechaInicial'], request.POST['fechaFinal']) == True:
                    requestObj = Solicitud()
                    requestObj.descripcion = 'Solicitud de Maquina'
                    requestObj.fechaInicial = request.POST['fechaInicial']
                    requestObj.fechaFinal = request.POST['fechaFinal']
                    if maquina.con_reserva == True:
                        requestObj.estado = 'creada'
                    else:
                        requestObj.estado = 'aprobada'
                    requestObj.solicitante = profile
                    requestObj.paso = Paso.objects.get(id = request.POST['step'])
                    requestObj.save()
                    maquinaRequest = SolicitudMaquina()
                    maquinaRequest.maquina = maquina
                    maquinaRequest.solicitud = requestObj
                    maquinaRequest.save()
                    messages.success(request, "La máquina se reservo exitosamente")
                    return redirect(reverse('Maquina-detail', kwargs = {'pk': request.GET.get('idAlmacenamiento', 0)}))
                else:
                    mensaje = "Ya existe una solicitud para estas fechas"

            contexto = {'form'        : form,
                        'mensaje'     : mensaje,
                        'maquina'     : maquina,
                        'proyectos'   : proyectos,
                        'maquinaEnLab': maquinaEnLab,
                        'start'       : request.GET.get('start', ''),
                        'end'         : request.GET.get('end', '')}
        except ObjectDoesNotExist:
            contexto = {'mensaje': 'No hay maquinas o pasos con el id solicitado'}
        except MultipleObjectsReturned:
            contexto = {'mensaje': 'Muchas maquinas con ese id'}
        return render(request, "solicitudes/crear_maquina_solicitud.html", contexto)
    else:
        return HttpResponse('No autorizado', status = 401)


def comprobarPostMaquina(form, formMaquina, formPos, request, template_name, section):
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

    if form.is_valid() and formPos.is_valid() and formMaquina.is_valid():
        mueble = form.save(commit = False)
        maquina = formMaquina.save(commit = False)
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
                mueble.save()
                maquina.mueble_id = mueble
                maquina.save()
                muebleEnLab.idMueble = mueble
                muebleEnLab.save()
                messages.success(request, "La máquina se añadio exitosamente")
                return redirect(reverse('maquina-update', kwargs = {'pk': maquina.pk}))
    else:
        form = MuebleForm()
        formMaquina = MaquinaForm()
        formPos = PosicionesMuebleForm()
    context = {'form'       : form,
               'formMaquina': formMaquina,
               'formPos'    : formPos,
               'section'    : section,
               }
    return render(request, template_name, context)
