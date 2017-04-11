# -*- coding: utf-8 -*-

"""Este módulo se encarga de generar las vistas a partir de los modelos, así como de hacer la lógica del negocio. """

__docformat__ = 'reStructuredText'

import datetime
import json

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from registration.backends.default.views import RegistrationView

from models import Bandeja, Projecto, MaquinaSolicitud, LaboratorioProfile
from models import Experimento
from models import LugarAlmacenamientoEnLab
from models import MaquinaEnLab
from models import MaquinaProfile
from models import Muestra
from models import MuestraSolicitud
from models import Paso
from models import Protocolo
from models import Solicitud
from models import Usuario
from .forms import LugarAlmacenamientoForm, SolicitudForm
from .forms import MuestraSolicitudForm
from .forms import PosicionesLugarAlmacenamientoForm
from .forms import RegistroUsuarioForm
from decimal import Decimal


# Create your views here.
def home(request):
    """Metodo inicial de la aplicación
               Se encarga de:
                   * Mostrar el inicio de la aplicación

            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :returns: HttpResponse -- La respuesta redirigiendo a la página home inicial de la aplicación
        """
    context = {}
    return render(request, "home.html", context)


class UserRegistrationView(RegistrationView):
    """Clase para el funcionamiento del regitro de usuario
            Historia de usuario: ALF-15:Yo como Usuario quiero ingresar al sistema con mis credenciales para acceder a todas las funcionalidades que el mismo tiene para mi.
            Se encarga de:
                * Ayuda al modelo de vista para renderizar la información del usuario

            :param RegistrationView: Clase que ayuda al modulo de registro de usuarios
            :type RegistrationView: RegistrationView.

        """
    form_class = RegistroUsuarioForm


@csrf_exempt
def registrar_usuario(request):
    """Registro de Usuarios
            Historia de usuario: ALF-15:Yo como Usuario quiero ingresar al sistema con mis credenciales para acceder a todas las funcionalidades que el mismo tiene para mi.
            Se encarga de:
                * Obtiene el formulario en el request
                * crea un usuario y un perfil

        :param request: El HttpRequest que se va a responder.
        :type request: HttpRequest.
        :returns: HttpResponse -- La respuesta a la peticion si sale bien, al home, sino al mismo formulario, si no tiene permisos responde no autorizado 
       """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addUser"):
        section = {}
        section['title'] = 'Agregar usuario'
        form = RegistroUsuarioForm(request.POST or None)
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            try:
                nuevo_perfil = User.objects.create_user(username=nuevo_usuario.nombre_usuario,
                                                        email=nuevo_usuario.correo_electronico,
                                                        password=nuevo_usuario.contrasena,
                                                        first_name=nuevo_usuario.nombres,
                                                        last_name=nuevo_usuario.apellidos
                                                        )
                nuevo_usuario.user = nuevo_perfil
                nuevo_usuario.user.groups.add(nuevo_usuario.grupo)
                nuevo_usuario.save()
                return HttpResponseRedirect(reverse('home'))
            except:
                form.add_error("userCode", "Un usuario con este id ya existe")
        context = {'form': form}
        return render(request, 'registration/registration_form.html', context)
    return HttpResponse('No autorizado', status=401)


def agregar_lugar(request):
    """Desplegar y comprobar los valores a insertar.
           Historia de usuario: ALF-37 - Yo como Jefe de Laboratorio quiero poder agregar nuevos lugares de almacenamiento para poder utilizarlos en el sistema.
           Se encarga de:
               * Mostar el formulario para agregar un lugar de almacenamiento.
               * Mostar el formulario para editar un lugar de almacenamiento ya existente.
               * Agregar un lugar de almacenamiento a la base de datos, agregar la relación entre lugar de almacenamiento y el laboratorio en el que está.

        :param request: El HttpRequest que se va a responder.
        :type request: HttpRequest.
        :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a la modificación del lugar de almacenamiento. Sino redirecciona al mismo formulario mostrando los errores.

       """
    mensaje = ""
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = LugarAlmacenamientoForm(request.POST, request.FILES)
            formPos = PosicionesLugarAlmacenamientoForm(request.POST or None, request.FILES or None)
            items = request.POST.get('items').split('\r\n')

            if form.is_valid() and formPos.is_valid():
                lugar = form.save(commit=False)
                lugarEnLab = formPos.save(commit=False)

                ocupado = MaquinaEnLab.objects.filter(idLaboratorio=lugarEnLab.idLaboratorio, xPos=lugarEnLab.posX,
                                                      yPos=lugarEnLab.posY).exists()
                # lamisma = MaquinaEnLab.objects.filter(pk=lugarEnLab.pk).exists()

                if ocupado:
                    formPos.add_error("posX", "La posición x ya esta ocupada")
                    formPos.add_error("posY", "La posición y ya esta ocupada")

                    mensaje = "El lugar en el que desea guadar ya esta ocupado"
                else:
                    mensaje = "La posición [" + str(lugarEnLab.posX) + "," + str(
                        lugarEnLab.posY) + "] no se encuentra en el rango del laboratorio"
                    lab = lugarEnLab.idLaboratorio
                    masX = lab.numX >= lugarEnLab.posX
                    masY = lab.numY >= lugarEnLab.posY
                    posible = masX and masY
                    if not posible:
                        if not masX:
                            formPos.add_error("posX", "La posición x sobrepasa el valor máximo de " + str(lab.numX))
                        if not masY:
                            formPos.add_error("posY", "La posición y sobrepasa el valor máximo de " + str(lab.numY))
                    else:
                        lugar.save()
                        lugarEnLab.idLugar = lugar
                        lugarEnLab.save()

                        if items is not None and len(items) > 0:
                            for item in items:
                                if item is not None and item != '':
                                    tamano = item.split(',')[0].split(':')[1]
                                    cantidad = item.split(',')[1].split(':')[1]
                                    bandeja = Bandeja(tamano=tamano, cantidad=cantidad, lugarAlmacenamiento=lugar,
                                                      libre=False)
                                    bandeja.save()

                        return HttpResponseRedirect(reverse('home'))
        else:
            form = LugarAlmacenamientoForm()
            formPos = PosicionesLugarAlmacenamientoForm()

        return render(request, 'LugarAlmacenamiento/agregar.html',
                      {'form': form, 'formPos': formPos, 'mensaje': mensaje})
    else:
        return HttpResponse('No autorizado', status=401)


class MaquinaForm(ModelForm):
    """Formulario  para crear y modificar una máquina.

          Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
                    
          Historia de usuario: `ALF-20 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-20 />`_ :Yo como Jefe de Laboratorio quiero poder filtrar las máquinas existentes por nombre para visualizar sólo las que me interesan.

          Historia de usuario: `ALF-25 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-25 />`_ :Yo como Asistente de Laboratorio quiero poder filtrar las máquinas existentes por nombre para visualizar sólo las que me interesan.

              Se encarga de:
                * Tener una instancia del modelo de la máquina
                * Seleccionar cuales campos del modelo seran desplegados en el formulario. Nombre, descripción, si esta reservado,activa
                  y la id dada por el sistema.
                * Agregar una máquina a la base de datos, agregar la relación entre la máquina y el laboratorio en el que está.
                * Modificar los datos  de una máquina ya existente.

           :param ModelForm: Instancia de Django.forms.
           :type ModelForm: ModelForm.

    """

    class Meta:
        model = MaquinaProfile
        fields = ['nombre', 'descripcion', 'con_reserva', 'activa', 'idSistema',
                  'imagen']


class PosicionesForm(ModelForm):
    """Formulario  para crear y modificar la ubicación de una máquina.
        Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
        Se encarga de:
            * Tener una instancia del modelo de la máquina en laboraotrio.
            * Definir las posición x, la posición y y el laboratorio en el cual se va aguardar la máquina.
            * Agregar una máquina a la base de datos, agregar la relación entre la máquina y el laboratorio en el que está.
            * Modificar la ubicación de una máquina ya existente.

     :param ModelForm: Instancia de Django.forms.
     :type ModelForm: ModelForm.

    """

    class Meta:
        model = MaquinaEnLab
        # fields=['xPos','yPos','idLaboratorio','idMaquina']
        exclude = ('idMaquina',)


def comprobarPostMaquina(form, formPos, request, template_name, section):
    """Desplegar y comprobar los valores a insertar.
        Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
        Se encarga de:
            * Mostar el formulario para agregar una máquina.
            * Mostar el formulario para editar una máquina ya existente.
            * Agregar una máquina a la base de datos, agregar la relación entre la máquina y el laboratorio en el que está.

     :param form: La información relevante de la máquina.
     :type form: MaquinaForm.
     :param formPos: La posición y el laboratorio en el que se va a guardar la máquina.
     :type formPos: PosicionesForm.
     :param request: El HttpRequest que se va a responder.
     :type request: HttpRequest.
     :param template_name: La template sobre la cual se va a renderizar.
     :type template_name: html.
     :param section: Objeto que permite diferenciar entre la modificación de una máquina y la adición de esta.
     :type section: {‘title’:,’agregar’}.
     :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a la modificación de la nueva máquina. Sino redirecciona al mismo formulario mostrand los errores.

    """
    mensaje = ""

    if form.is_valid() and formPos.is_valid():
        new_maquina = form.save(commit=False)
        new_maquinaEnLab = formPos.save(commit=False)
        xPos = new_maquinaEnLab.xPos
        yPos = new_maquinaEnLab.yPos
        ocupadoX = MaquinaEnLab.objects.filter(idLaboratorio=new_maquinaEnLab.idLaboratorio, xPos=xPos).exists()
        ocupadoY = MaquinaEnLab.objects.filter(idLaboratorio=new_maquinaEnLab.idLaboratorio, yPos=yPos).exists()
        # lamisma=MaquinaEnLab.objects.filter(idLaboratorio=new_maquinaEnLab.idLaboratorio, yPos=yPos,xPos=xPos,idMaquina).exists()
        lamisma = MaquinaEnLab.objects.filter(pk=new_maquinaEnLab.pk).exists()
        if (ocupadoX and ocupadoY) and not lamisma:
            if (ocupadoX):
                formPos.add_error("xPos", "La posición x ya esta ocupada")
            if (ocupadoY):
                formPos.add_error("yPos", "La posición y ya esta ocupada")
            mensaje = "El lugar en el que desea guadar ya esta ocupado"
        else:
            mensaje = "La posición [" + str(xPos) + "," + str(yPos) + "] no se encuentra en el rango del labortorio"
            lab = new_maquinaEnLab.idLaboratorio
            masX = lab.numX >= xPos
            masY = lab.numY >= yPos
            posible = masX and masY
            if not posible:
                if not masX:
                    formPos.add_error("xPos", "La posición x sobrepasa el valor máximo de " + str(lab.numX))
                if not masY:
                    formPos.add_error("yPos", "La posición y sobrepasa el valor máximo de " + str(lab.numY))
            else:
                new_maquina.save()
                new_maquinaEnLab.idMaquina = new_maquina
                new_maquinaEnLab.save()
                return redirect(reverse('maquina-update', kwargs={'pk': new_maquina.pk}))

    return render(request, template_name,
                  {'form': form, 'formPos': formPos, 'section': section, 'mensaje': mensaje})


def maquina_create(request, template_name='Maquinas/agregar.html'):
    """Comporbar si el usuario puede agregar una máquina y obtener los campos necesarios.
        Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
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
     :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a la modificación de la nueva
                               máquina. Sino redirecciona al mismo formulario mostrando los errores. Si no esta autorizado se envia un código 401

    """

    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_addMachine"):
        section = {}
        section['title'] = 'Agregar máquina'
        section['agregar'] = True
        form = MaquinaForm(request.POST or None, request.FILES or None)
        formPos = PosicionesForm(request.POST or None, request.FILES or None)
        return comprobarPostMaquina(form, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status=401)


def maquina_update(request, pk, template_name='Maquinas/agregar.html'):
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
     :returns: HttpResponse -- La respuesta a la petición, en caso de que todo salga bien redirecciona a si mismo. Sino redirecciona al mismo formulario mostrando los errores. Si no esta autorizado se envia un código 401

    """

    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_edditMachine"):
        server = get_object_or_404(MaquinaProfile, pk=pk)
        serverRelacionLab = get_object_or_404(MaquinaEnLab, idMaquina=server)
        mensaje = ""
        form = MaquinaForm(request.POST or None, request.FILES or None, instance=server)
        formPos = PosicionesForm(request.POST or None, request.FILES or None, instance=serverRelacionLab)
        section = {}
        section['title'] = 'Modificar máquina'
        section['agregar'] = False
        return comprobarPostMaquina(form, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status=401)


def listarMaquinas(request):
    """Comprobar si el usario puede ver las máquinas y mostraselas filtrando por una búsqueda.
        Historia de usuario: ALF-20:Yo como Jefe de Laboratorio quiero poder filtrar las máquinas existentes por nombre para visualizar sólo las que me interesan.
        Historia de usuario: ALF-25:Yo como Asistente de Laboratorio quiero poder filtrar las máquinas existentes por nombre para visualizar sólo las que me interesan.
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
     :returns: HttpResponse -- La respuesta a la petición. Retorna páginada la lista de las máquias que cumplen con la búsqueda. Si no esta autorizado se envia un código 401

    """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_viewMachine"):
        edita=request.user.has_perm("LabModule.can_edditMachine")
        pag = request.GET.get('pag', 1)
        que = request.GET.get("que", "")
        numer = int(request.GET.get("num", "10"))
        section = {}
        section['title'] = 'Máquinas'
        if not edita:
          lista_maquinas = MaquinaProfile.objects.all().filter(nombre__icontains=que,activa=True).extra(order_by=['nombre'])
        else:
          lista_maquinas = MaquinaProfile.objects.all().filter(nombre__icontains=que).extra(order_by=['nombre'])

        paginatorMaquinas = Paginator(lista_maquinas, numer)
        try:
            maquinas = paginatorMaquinas.page(pag)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            maquinas = paginatorMaquinas.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            maquinas = paginatorMaquinas.page(paginatorMaquinas.num_pages)

        idMquinas = [maquina.idSistema for maquina in maquinas]
        lista_Posiciones = MaquinaEnLab.objects.all().filter(idMaquina__in=idMquinas)
        paginas = [x + 1 for x in range(maquinas.paginator.num_pages)]
        maquinasConUbicacion = zip(maquinas.object_list, lista_Posiciones)
        context = {'paginas': paginas, 'pag': int(pag), 'last': maquinas.paginator.num_pages, 'section': section,
                   'maquinasBien': maquinasConUbicacion, "query": que}
        return render(request, 'Maquinas/ListaMaquinas.html', context)
    return HttpResponse('No autorizado', status=401)


def listar_lugares(request):
    """Desplegar y comprobar los valores a consultar.
              Historia de usuario: ALF-39 - Yo como Jefe de Laboratorio quiero poder filtrar los lugares de almacenamiento existentes por nombre para visualizar sólo los que me interesan.
              Se encarga de:
                  * Mostar el formulario para consultar los lugares de almacenamiento.

           :param request: El HttpRequest que se va a responder.
           :type request: HttpRequest.
           :returns: HttpResponse -- La respuesta a la petición, con información de los lugares de almacenamiento existentes.

          """
    if request.user.is_authenticated():
        lista_lugares = LugarAlmacenamientoEnLab.objects.all()
        context = {'lista_lugares': lista_lugares}
        return render(request, 'LugarAlmacenamiento/listar.html', context)
    else:
        return HttpResponse('No autorizado', status=401)


def crear_solicitud_maquina(request):
    """Realiza la solicitud de máquinas por el usuario que la necesita
        Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una franja de tiempo especifica para hacer uso de ella
        Se encarga de:
            * Comprobar si hay un usuario logueado
            * Comprobar si el usuario tiene permisos para realizar la solicitud de máquinas
            * Realizar la solicitud de máquinas

     :param request: El HttpRequest que se va a responder.
     :type request: HttpRequest.

     :returns: HttpResponse -- La respuesta a la petición. Si no esta autorizado se envia un código 401

    """
    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_solMaquina"):
        mensaje = 'ok'
        contexto = {}
        try:

            maquina = MaquinaProfile.objects.get(pk=request.GET.get('id', 0), activa=True)
            profile = Usuario.objects.get(user_id=request.user.id)
            maquinaEnLab = MaquinaEnLab.objects.get(idMaquina=maquina.pk)
            proyectos = Projecto.objects.filter(asistentes=profile.id, activo=True)
            form = SolicitudForm()
            if request.method == 'POST':
                if form.verificar_fecha(maquina.pk, request.POST['fechaInicial'], request.POST['fechaFinal']) == True:
                    requestObj = Solicitud()
                    requestObj.descripcion = 'Solicitud de maquina'
                    requestObj.fechaInicial = request.POST['fechaInicial']
                    requestObj.fechaFinal = request.POST['fechaFinal']
                    if maquina.con_reserva == True:
                        requestObj.estado = 'creada'
                    else:
                        requestObj.estado = 'aprobada'
                    requestObj.solicitante = profile.id
                    requestObj.paso = Paso.objects.get(id=request.POST['step'])
                    requestObj.save()
                    maquinaRequest = MaquinaSolicitud()
                    maquinaRequest.maquina = maquina
                    maquinaRequest.solicitud = requestObj
                    maquinaRequest.save()
                    return redirect("../")
                else:
                    mensaje = "ya existe una solicitud para estas fechas"

            contexto = {'form': form, 'mensaje': mensaje, 'maquina': maquina, 'proyectos': proyectos,
                        'maquinaEnLab': maquinaEnLab}
        except ObjectDoesNotExist as e:
            contexto = {'mensaje': 'No hay maquinas o pasos con el id solicitado'}
        except MultipleObjectsReturned as e:
            contexto = {'mensaje': 'Muchas maquinas con ese id'}
        return render(request, "Solicitudes/crear_maquina_solicitud.html", contexto)
    else:
        return HttpResponse('No autorizado', status=401)


def listar_lugar(request, pk):
    """Desplegar y comprobar los valores a consultar.
                Historia de usuario: ALF-42-Yo como Jefe de Laboratorio quiero poder ver el detalle de un lugar de almacenamiento para conocer sus características
                Se encarga de:
                * Mostar el formulario para consultar los lugares de almacenamiento.

            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.
            :param pk: La llave primaria del lugar de almacenamiento
            :type pk: String.
            :returns: HttpResponse -- La respuesta a la petición, con información de los lugares de almacenamiento existentes.
        """
    if request.user.is_authenticated():
        lista_lugar = LugarAlmacenamientoEnLab.objects.filter(idLugar_id=pk)
        if lista_lugar is None:
            return listar_lugares(request)
        else:
            lugar = lista_lugar[0]
            bandejasOcupadas = Bandeja.objects.filter(lugarAlmacenamiento_id=pk, libre=False).count()
            bandejasLibres = Bandeja.objects.filter(lugarAlmacenamiento_id=pk, libre=True).count()
            #tamano = 0
            #lista = Bandeja.objects.filter(lugarAlmacenamiento_id=pk)

            #for x in lista:
                #tamano += Decimal(x.tamano)

            laboratorio = LaboratorioProfile.objects.get(pk=lugar.idLaboratorio_id).nombre

            context = {'lugar': lugar, 'bandejasOcupadas': bandejasOcupadas, 'bandejasLibres': bandejasLibres,
                        'laboratorio': laboratorio}
            return render(request, 'LugarAlmacenamiento/detalle.html', context)
    else:
        return HttpResponse('No autorizado', status=401)


def crear_solicitud_muestra(request):
    """Realiza la solicitud de muestras por el usuario que la necesita
            Historia de usuario: ALF-81:Yo como Asistente de Laboratorio quiero poder solicitar una muestra para continuar con mis experimentos
            Se encarga de:
                * Comprobar si hay un usuario logueado
                * Comprobar si el usuario tiene permisos para realizar la solicitud de muestras
                * Realizar la solicitud de muestras

         :param request: El HttpRequest que se va a responder.
         :type request: HttpRequest.

         :returns: HttpResponse -- La respuesta a la petición. Si no esta autorizado se envia un código 401

    """

    if request.user.is_authenticated() and request.user.has_perm("LabModule.can_solMuestra"):
        mensaje = 'ok'
        contexto = {}
        try:

            muestra = Muestra.objects.get(id=request.GET.get('id', 0), activa=True)
            profile = Usuario.objects.get(user_id=request.user.id)
            proyectos = Projecto.objects.filter(asistentes=profile.id, activo=True);

            muestra = Muestra.objects.get(id=request.GET.get('id', 0))
            profile = Usuario.objects.get(user_id=request.user.id)

            if request.method == 'POST':

                requestObj = Solicitud()
                requestObj.descripcion = 'Solicitud de uso de muestra'
                requestObj.fechaInicial = request.POST['fechaInicial']
                requestObj.estado = 'creada'
                requestObj.solicitante = profile.id
                requestObj.paso = Paso.objects.get(id=request.POST['step'])
                requestObj.save()
                sampleRequest = MuestraSolicitud()
                sampleRequest.solicitud = requestObj
                sampleRequest.muestra = muestra
                sampleRequest.cantidad = request.POST['cantidad']
                sampleRequest.tipo = 'uso'
                sampleRequest.save()
                return redirect("../")

            else:
                form = SolicitudForm()
                form_muestra = MuestraSolicitudForm()
            contexto = {'form': form, 'mensaje': mensaje, 'muestra': muestra, 'proyectos': proyectos,
                        'form_muestra': form_muestra}
        except ObjectDoesNotExist as e:
            contexto = {'mensaje': 'No hay muestras o pasos con el id solicitado'}

        except MultipleObjectsReturned as e:
            contexto = {'mensaje': 'Muchas muestras con ese id'}

        return render(request, "Solicitudes/crear_muestra_solicitud.html", contexto)
    else:
        return HttpResponse('No autorizado', status=401)


def poblar_datos(request):
    """Realiza la población de datos para máquinas
            Historia de usuario: `ALF-18 <http://miso4101-2.virtual.uniandes.edu.co:8080/browse/ALF-18 />`_ :Yo como Jefe de Laboratorio quiero poder agregar nuevas máquinas en el sistema para que puedan ser usadas por los asistentes.
            Se encarga de:
                * Poblar la información para las máquinas

            :param request: El HttpRequest que se va a responder.
            :type request: HttpRequest.

            :returns: HttpResponse -- Redirección a la pagina inicial de la aplicación

        """
    MaquinaProfile.objects.create(
        nombre='Laboratorio genomica',
        descripcion="Aca se hace genomica",
        idSistema="Lab_101")
    return HttpResponseRedirect(reverse('home'))


@csrf_exempt
def cargar_experimentos(request):
    """Realiza el cargue de datos de experimentos existentes por identificador del proyecto
                Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una franja de tiempo especifica para hacer uso de ella
                Se encarga de:
                    * Cargue de datos de experimentos
                :param request: El HttpRequest que se va a responder.
                :type request: HttpRequest.

                :returns: HttpResponse -- La información de experimentos existentes por identificador del proyecto

            """
    if request.GET['project_id'] != "":
        experiments = Experimento.objects.filter(projecto=request.GET['project_id'])
        experimentsDict = dict([(c.id, c.nombre) for c in experiments])
        return HttpResponse(json.dumps(experimentsDict))
    else:
        return HttpResponse()


@csrf_exempt
def cargar_protocolos(request):
    """Realiza el cargue de datos de protocolos existentes por identificador del experimento
                  Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una franja de tiempo especifica para hacer uso de ella
                  Se encarga de:
                      * Cargue de datos de protocolos
                  :param request: El HttpRequest que se va a responder.
                  :type request: HttpRequest.

                  :returns: HttpResponse -- La información de protocolos existentes por identificador del experimento

              """
    if request.GET['experiment_id'] != "":
        protocols = Protocolo.objects.filter(experimento=request.GET['experiment_id'])
        protocolsDict = dict([(c.id, c.nombre) for c in protocols])
        return HttpResponse(json.dumps(protocolsDict))
    else:
        return HttpResponse()


@csrf_exempt
def cargar_pasos(request):
    """Realiza el cargue de datos de pasos existentes por identificador del protocolo
                    Historia de usuario: ALF-4:Yo como Asistente de Laboratorio quiero solicitar una maquina normal en una franja de tiempo especifica para hacer uso de ella
                    Se encarga de:
                        * Cargue de datos de pasos
                    :param request: El HttpRequest que se va a responder.
                    :type request: HttpRequest.

                    :returns: HttpResponse -- La información de pasos existentes por identificador del protocolo

                """
    if request.GET['protocol_id'] != "":
        steps = Paso.objects.filter(protocolo=request.GET['protocol_id'])
        stepsDict = dict([(c.id, c.nombre) for c in steps])
        return HttpResponse(json.dumps(stepsDict))
    else:
        return HttpResponse()
