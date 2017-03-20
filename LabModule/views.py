# -*- coding: utf-8 -*-

"""Este módulo se encarga de generar las vistas a partir de los modelos, así como de hacer la lógica del negocio. """

__docformat__ = 'reStructuredText'

import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import ModelForm, models
from django import forms

from django.views.decorators.csrf import csrf_exempt
from models import MaquinaProfile, Bandeja, LugarAlmacenamiento, Sample, UserProfile, Step, SampleRequest, Experiment, \
    Protocol, Request, MaquinaEnLab,LaboratorioProfile
from django.http import HttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from registration.backends.default.views import RegistrationView
from .forms import UserProfileForm, LugarAlmacenamientoForm, SampleRequestForm


# Create your views here.
def home(request):
    context = {}
    return render(request, "home.html", context)


def agregar_lugar(request):
    if request.method == 'POST':
        form = LugarAlmacenamientoForm(request.POST, request.FILES)
        items = request.POST.get('items').split('\r\n')

        if form.is_valid():
            lugar = form.save()

            if items is not None and len(items) > 0:
                for item in items:
                    if item is not None and item != '':
                        tamano = item.split(',')[0].split(':')[1]
                        cantidad = item.split(',')[1].split(':')[1]
                        bandeja = Bandeja(tamano=tamano, cantidad=cantidad, lugarAlmacenamiento=lugar)
                        bandeja.save()

            return HttpResponseRedirect(reverse('home'))
    else:
        form = LugarAlmacenamientoForm()

    return render(request, 'LugarAlmacenamiento/agregar.html', {'form': form})



class MaquinaForm(ModelForm):
    """Formulario  para crear y modificar una máquina.

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

        Se encarga de:
            * Tener una instancia del modelo de la máquina en laboraotrio.
            * Definir las posición x, la posición y y el laboratorio en el cual se va aguardar la máquina.
            * Agregar una máquina a la base de datos, agregar la relación entre la máquina y el laboratorio en el que está.
            * Modificar la ubicación de una máquina ya existente.

     :param ModelForm: Instancia de Django.forms.
     :type ModelForm: ModelForm.

    """
    class Meta:
        model=MaquinaEnLab
        #fields=['xPos','yPos','idLaboratorio','idMaquina']
        exclude = ('idMaquina',)



def comprobarPostMaquina(form,formPos,request,template_name,section):
    """Desplegar y comprobar los valores a insertar.

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
        #lamisma=MaquinaEnLab.objects.filter(idLaboratorio=new_maquinaEnLab.idLaboratorio, yPos=yPos,xPos=xPos,idMaquina).exists()
        lamisma = MaquinaEnLab.objects.filter(pk=new_maquinaEnLab.pk).exists()
        if (ocupadoX or ocupadoY) and not lamisma:
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

    if request.user.is_authenticated() and request.user.has_perm("account.can_addMachine"):
        section = {}
        section['title'] = 'Agregar máquina'
        section['agregar'] = True
        form = MaquinaForm(request.POST or None, request.FILES or None)
        formPos = PosicionesForm(request.POST or None, request.FILES or None)
        return comprobarPostMaquina(form, formPos,request,template_name,section)
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

    if request.user.is_authenticated() and request.user.has_perm("account.can_edditMachine"):
        server = get_object_or_404(MaquinaProfile, pk=pk)
        serverRelacionLab = get_object_or_404(MaquinaEnLab, idMaquina=server)
        mensaje=""
        form = MaquinaForm(request.POST or None, request.FILES or None, instance=server)
        formPos = PosicionesForm(request.POST or None, request.FILES or None,instance=serverRelacionLab)
        section = {}
        section['title'] = 'Modificar máquina'
        section['agregar'] = False
        return comprobarPostMaquina(form, formPos, request, template_name, section)
    else:
        return HttpResponse('No autorizado', status=401)



class UserRegistrationView(RegistrationView):
    form_class = UserProfileForm


def listar_lugares(request):
    lista_lugares = LugarAlmacenamiento.objects.all()
    context = {'lista_lugares': lista_lugares}
    return render(request, 'LugarAlmacenamiento/listar.html', context)


def make_sample_request(request):
    message = 'ok'
    try:

        sample = Sample.objects.get(id=request.GET.get('id', 0))
        profile = UserProfile.objects.get(user_id=request.user.id)

        if request.method == 'POST':

            requestObj = Request()
            requestObj.description = 'Solicitud de uso de muestra'
            requestObj.initialDate = request.POST['dateIni_year'] + "-" + request.POST['dateIni_month'] + "-" + \
                                     request.POST['dateIni_day']
            requestObj.state = 'open'
            requestObj.applicant = profile.id
            requestObj.actualDate = datetime.date.today()
            requestObj.step = Step.objects.get(id=request.POST['step'])
            requestObj.save()
            sampleRequest = SampleRequest()
            sampleRequest.request = requestObj
            sampleRequest.sample = sample
            sampleRequest.quantity = request.POST['quantity']
            sampleRequest.type = 'uso'
            sampleRequest.save()
            return redirect("../")

        else:
            form = SampleRequestForm(sample, profile.id)

    except ObjectDoesNotExist as e:
        form = {}
        message = 'No hay muestras o pasos con el id solicitado'
    except MultipleObjectsReturned as e:
        form = {}
        message = 'Muchas muestras con ese id'
    return render(request, "Solicitudes/make_sample_request.html", {'form': form, 'message': message})


@csrf_exempt
def get_experiments(request):
    if request.GET['project_id'] != "":
        experiments = Experiment.objects.filter(project=request.GET['project_id'])
        experimentsDict = dict([(c.id, c.name) for c in experiments])
        return HttpResponse(json.dumps(experimentsDict))
    else:
        return HttpResponse()


@csrf_exempt
def get_protocols(request):
    if request.GET['experiment_id'] != "":
        protocols = Protocol.objects.filter(experiment=request.GET['experiment_id'])
        protocolsDict = dict([(c.id, c.name) for c in protocols])
        return HttpResponse(json.dumps(protocolsDict))
    else:
        return HttpResponse()


@csrf_exempt
def get_steps(request):
    if request.GET['protocol_id'] != "":
        steps = Step.objects.filter(protocol=request.GET['protocol_id'])
        stepsDict = dict([(c.id, c.name) for c in steps])
        return HttpResponse(json.dumps(stepsDict))
    else:
        return HttpResponse()
