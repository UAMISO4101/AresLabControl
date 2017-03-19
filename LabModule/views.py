import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from registration.views import RegistrationView

from LabModule import models
from LabModule.forms import SampleRequestForm, UserProfileForm
from LabModule.models import Sample, UserProfile, Tray, Project, Experiment, Protocol, Step, SampleRequest


def home(request):
    context = {}

    return render(request, "home.html", context)

def make_sample_request(request):
    message='ok'
    try:
        sample = Sample.objects.get(id=request.GET['id'])
        profile = UserProfile.objects.get(user_id=request.user.id)
        if request.method == 'POST':
            requestObj = models.Request()
            requestObj.description= 'Solicitud de uso de muestra'
            requestObj.initialDate= request.POST['dateIni_year']+"-"+request.POST['dateIni_month']+"-"+request.POST['dateIni_day']
            requestObj.state='open'
            requestObj.applicant= profile.id
            requestObj.actualDate= datetime.date.today()
            requestObj.step= Step.objects.get(id=request.POST['step'])
            requestObj.save()
            sampleRequest= SampleRequest()
            sampleRequest.request=requestObj
            sampleRequest.sample=sample
            sampleRequest.quantity=request.POST['quantity']
            sampleRequest.type='uso'
            sampleRequest.save()
            return redirect("../")

        else:
            form = SampleRequestForm(sample, profile.id)

    except ObjectDoesNotExist as e:
        form = {}
        message = 'No hay muestras con el id solicitado'
    except MultipleObjectsReturned as e:
        form = {}
        message = 'Muchas mjuestras con ese id'
    return render(request, "Solicitudes/make_sample_request.html", {'form': form, 'message': message})


@csrf_exempt
def get_experiments(request):
    if request.GET['project_id']!="":
        experiments = Experiment.objects.filter(project=request.GET['project_id'])
        experimentsDict = dict([(c.id, c.name) for c in experiments])
        return HttpResponse(json.dumps(experimentsDict))
    else:
        return HttpResponse()
@csrf_exempt
def get_protocols(request):
    if request.GET['experiment_id']!="":
        protocols = Protocol.objects.filter(experiment=request.GET['experiment_id'])
        protocolsDict = dict([(c.id, c.name) for c in protocols])
        return HttpResponse(json.dumps(protocolsDict))
    else:
        return HttpResponse()
@csrf_exempt
def get_steps(request):
    if request.GET['protocol_id']!="":
        steps = Step.objects.filter(protocol=request.GET['protocol_id'])
        stepsDict = dict([(c.id, c.name) for c in steps])
        return HttpResponse(json.dumps(stepsDict))
    else:
        return HttpResponse()


def agregar_lugar(request):
    return render(request, 'LugarAlmacenamiento/agregar.html')

class UserRegistrationView(RegistrationView):
    form_class = UserProfileForm


