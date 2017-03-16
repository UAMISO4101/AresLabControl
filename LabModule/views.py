from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render


# Create your views here.
from registration.views import RegistrationView

from LabModule.forms import SampleRequestForm, UserProfileForm
from LabModule.models import Sample


def home(request):
    context = {}

    return render(request, "home.html", context)

def make_sample_request(request):

    try:
        sample = Sample.objects.get(id=1)
        form = SampleRequestForm(sample)
    except ObjectDoesNotExist as e:
        form= 'No hay muestras con el id solicitado'
    except MultipleObjectsReturned as e:
        form = 'Muchas mjuestras con ese id'

    return render(request, "Solicitudes/make_sample_request.html", {'form': form})


def agregar_lugar(request):
    return render(request, 'LugarAlmacenamiento/agregar.html')

class UserRegistrationView(RegistrationView):
    form_class = UserProfileForm


