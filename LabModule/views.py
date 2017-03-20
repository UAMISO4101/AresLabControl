# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import ModelForm, models
from django import forms

from django.views.decorators.csrf import csrf_exempt
from models import MaquinaProfile, Bandeja, LugarAlmacenamiento, Sample, UserProfile, Step, SampleRequest, Experiment, \
    Protocol, Request, MaquinaEnLab
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


def agregar_maquina(request):
    return render(request, 'Maquinas/agregar.html')


class MaquinaForm(ModelForm):
    class Meta:
        model = MaquinaProfile
        fields = ['nombre', 'laboratorio', 'descripcion', 'con_reserva', 'activa', 'idSistema', 'xPos', 'yPos',
                  'imagen']


def maquina_create(request, template_name='Maquinas/agregar.html'):
    if request.user.is_authenticated() and request.user.has_perm("account.can_addMachine"):
        form = MaquinaForm(request.POST or None, request.FILES)
        section = {}
        section['title'] = 'Agregar máquina'
        section['agregar'] = True
        if form.is_valid():
            new_maquina = form.save(commit=False)
            ocupado=MaquinaEnLab.objects.filter().exists()
            print ocupado
            if ocupado:
                mensaje="El lugar en el que desea guadar ya esta ocupado"
                return render(request, template_name, {'form': form, 'section': section,'mensaje':mensaje})
            else:
                new_maquina = form.save()
                return redirect(reverse('maquina-update', kwargs={'pk': new_maquina.pk}))
        return render(request, template_name, {'form': form, 'section': section})
    else:
        return HttpResponse('No autorizado', status=401)


def maquina_update(request, pk, template_name='Maquinas/agregar.html'):
    if request.user.is_authenticated() and request.user.has_perm("account.can_edditMachine"):
        server = get_object_or_404(MaquinaProfile, pk=pk)
        form = MaquinaForm(request.POST or None, request.FILES or None, instance=server)
        section = {}
        section['title'] = 'Modificar máquina'
        section['agregar'] = False
        if form.is_valid():
            form.save()
            return redirect(reverse('maquina-update', kwargs={'pk': pk}))
        return render(request, template_name, {'form': form, 'section': section, 'server': server})
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
