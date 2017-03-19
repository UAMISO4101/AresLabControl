# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from models import MaquinaProfile, Bandeja, LugarAlmacenamiento
from django.http import HttpResponse

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


def listar_lugares(request):
    lista_lugares = LugarAlmacenamiento.objects.all()
    context = {'lista_lugares': lista_lugares}
    return render(request, 'LugarAlmacenamiento/listar.html', context)
