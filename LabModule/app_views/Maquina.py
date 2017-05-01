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
from LabModule.app_forms.Maquina import PosicionesMaquinaForm
from LabModule.app_forms.Solicitud import SolicitudForm
from LabModule.app_models.Maquina import Maquina
from LabModule.app_models.MaquinaEnLab import MaquinaEnLab
from LabModule.app_models.Paso import Paso
from LabModule.app_models.Proyecto import Proyecto
from LabModule.app_models.Solicitud import Solicitud
from LabModule.app_models.SolicitudMaquina import SolicitudMaquina
from LabModule.app_models.Usuario import Usuario
from LabModule.app_views.Almacenamiento import lugar_list


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
        maquina = get_object_or_404(Maquina, pk = pk)
        maquinaEnLab = get_object_or_404(MaquinaEnLab, idMaquina = maquina)
        mensaje = ""
        section = {'title': 'Ver detalle ', 'agregar': "ver"}
        mensajeCalendario = "Este es el horario disponible de la máquina. Seleccione el horario que más le convenga"
        return render(request, template_name,
                      {'Maquina': maquina, 'maquinaEnLab': maquinaEnLab, 'section': section,
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
        server = get_object_or_404(Maquina, pk = pk)
        serverRelacionLab = get_object_or_404(MaquinaEnLab, idMaquina = server)
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
        contexto = {'start': request.GET.get('start', ''), 'end': request.GET.get('end', '')}

        try:

            maquina = Maquina.objects.get(pk = request.GET.get('id', 0), activa = True)
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
                    return redirect(reverse('Maquina-detail', kwargs = {'pk': request.GET.get('id', 0)}))
                else:
                    mensaje = "Ya existe una solicitud para estas fechas"

            contexto = {'form'        : form, 'mensaje': mensaje, 'Maquina': maquina, 'proyectos': proyectos,
                        'maquinaEnLab': maquinaEnLab, 'start': request.GET.get('start', ''),
                        'end'         : request.GET.get('end', '')}
        except ObjectDoesNotExist as e:
            print (e.message)
            contexto = {'mensaje': 'No hay maquinas o pasos con el id solicitado'}
        except MultipleObjectsReturned as e:
            print(e.message)
            contexto = {'mensaje': 'Muchas maquinas con ese id'}
        return render(request, "solicitudes/crear_maquina_solicitud.html", contexto)
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
                return redirect(reverse('Maquina-update', kwargs = {'pk': new_maquina.pk}))

    return render(request, template_name,
                  {'form': form, 'formPos': formPos, 'section': section, 'mensaje': mensaje})
