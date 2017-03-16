from django.shortcuts import render
from registration.backends.default.views import RegistrationView
from .forms import UserProfileForm


# Create your views here.
def home(request):
    context = {}
    return render(request, "home.html", context)


def agregar_lugar(request):
    return render(request, 'LugarAlmacenamiento/agregar.html')


class UserRegistrationView(RegistrationView):
    form_class = UserProfileForm
