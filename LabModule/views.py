from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from registration.backends.default.views import RegistrationView
from .forms import UserProfileForm, LugarAlmacenamientoForm


# Create your views here.
def home(request):
    context = {}
    return render(request, "home.html", context)


def agregar_lugar(request):
    if request.method == 'POST':
        form = LugarAlmacenamientoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('home'))
    else:
        form = LugarAlmacenamientoForm()

    return render(request, 'LugarAlmacenamiento/agregar.html', {'form': form})


class UserRegistrationView(RegistrationView):
    form_class = UserProfileForm
