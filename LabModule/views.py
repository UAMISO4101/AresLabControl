# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from models import MaquinaProfile

# Create your views here.
def home(request):
    context = {}

    return render(request, "home.html", context)

def agregar_lugar(request):
    return render(request, 'LugarAlmacenamiento/agregar.html')

def agregar_maquina(request):

    return render(request, 'Maquinas/agregar.html')

class MaquinaForm(ModelForm):
    class Meta:
        model = MaquinaProfile
        fields = ['nombre','laboratorio','descripcion','idSistema','xPos','yPos','imagen']

def maquina_create(request,template_name = 'Maquinas/agregar.html'):
    form = MaquinaForm(request.POST or None,request.FILES)
    section={}
    section['title']='Agregar máquina'
    section['agregar'] = True
    if form.is_valid():
        new_maquina = form.save()
        return redirect(reverse('maquina-update',kwargs={'pk':new_maquina.pk}))
    return render(request, template_name, {'form': form,'section':section})

def maquina_update(request, pk, template_name='Maquinas/agregar.html'):
    server = get_object_or_404(MaquinaProfile, pk=pk)
    form = MaquinaForm(request.POST or None, request.FILES or None, instance=server)
    section={}
    section['title']='Modificar máquina'
    section['agregar'] = False
    if form.is_valid():
        form.save()
        return redirect(reverse('maquina-update',kwargs={'pk':pk}))
    return render(request, template_name, {'form':form,'section':section,'server':server})