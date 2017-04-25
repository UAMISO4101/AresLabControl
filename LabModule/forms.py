# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms import ModelForm

from .models import LugarAlmacenamiento
from .models import LugarAlmacenamientoEnLab
from .models import MaquinaEnLab
from .models import MaquinaProfile
from .models import MaquinaSolicitud
from .models import Muestra
from .models import MuestraSolicitud
from .models import Solicitud
from .models import Usuario


class RegistroUsuarioForm(forms.ModelForm):
    """Formulario  para crear usuarios.
           Se encarga de:
               * Tener una instancia del modelo del usuario.
               * Agregar un usuario a la base de datos.
        :param ModelForm: Instancia de Django.forms.
        :type ModelForm: ModelForm.
       """

    class Meta:
        model = Usuario
        exclude = ('user',)

    contrasena = forms.CharField(
            label = "Escriba su contraseña",
            widget = forms.PasswordInput,
            strip = False, )
    password2 = forms.CharField(
            label = "Confirme su contraseña",
            widget = forms.PasswordInput,
            strip = False,
            help_text = "Repita la contraseña para verificar que sean iguales.",
    )

    error_messages = {
        'password_mismatch': "Las contraseñas deben coincidir!",
    }

    def clean_password2(self):
        # Check that the two password entries match
        contrasena = self.cleaned_data.get("contrasena")
        password2 = self.cleaned_data.get("password2")
        if contrasena and password2 and contrasena != password2:
            raise forms.ValidationError("Las contraseñas no coinciden!")
        return contrasena


class LugarAlmacenamientoForm(ModelForm):
    """Formulario  para crear y modificar el lugar almacenamiento.
           Se encarga de:
               * Tener una instancia del modelo del lugar almacenamiento en laboraotrio.
               * Agregar un lugar almacenamiento a la base de datos.
               * Modificar un lugar almacenamiento ya existente.
        :param ModelForm: Instancia de Django.forms.
        :type ModelForm: ModelForm.
       """

    class Meta:
        model = LugarAlmacenamiento
        fields = ['id','nombre', 'descripcion', 'capacidad', 'temperatura', 'imagen']


class PosicionesAlmacenamientoForm(ModelForm):
    """Formulario  para crear y modificar la ubicación de un lugar almacenamiento.
        Se encarga de:
            * Tener una instancia del modelo del lugar almacenamiento en laboratorio.
            * Definir las posición x, la posición y y el laboratorio en el cual se va aguardar el lugar almacenamiento.
            * Agregar un lugar almacenamiento a la base de datos, agregar la relación entre el lugar almacenamiento y el laboratorio en el que está.
            * Modificar la ubicación de un lugar almacenamiento ya existente.
     :param ModelForm: Instancia de Django.forms.
     :type ModelForm: ModelForm.
    """

    class Meta:
        model = LugarAlmacenamientoEnLab
        fields = ['posX', 'posY', 'idLaboratorio']
        exclude = ('idLugar',)


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fechaInicial', 'fechaFinal', 'descripcion', 'estado', 'solicitante', 'fechaActual', 'paso']
        widgets = {
            'fechaInicial': forms.DateInput(attrs = {'class': 'form-control date '},format= ("%Y-%m-%d %H:%m")),
            'fechaFinal'  : forms.DateInput(attrs = {'class': 'form-control date '},format= ("%Y-%m-%d %H:%m")),
        }

    def verificar_fecha(self, maquina_id, fechaIni, fechaFin):

        solicitudes = Solicitud.objects.filter(
                Q(fechaInicial = fechaIni, fechaFinal = fechaFin) | Q(fechaInicial__lt = fechaIni,
                                                                      fechaFinal__gt = fechaIni) | Q(
                        fechaInicial__lte = fechaFin, fechaFinal__gte = fechaFin)).exclude(estado = 'rechazada')
        for sol in solicitudes:
            otras_maquinas = MaquinaSolicitud.objects.filter(solicitud = sol.pk, maquina = maquina_id).count()
            if otras_maquinas > 0:
                return False
        return True


class MuestraSolicitudForm(ModelForm):
    class Meta:
        model = MuestraSolicitud
        fields = ['cantidad', 'solicitud', 'muestra', 'tipo']
        widgets = {
            'cantidad': forms.TextInput(attrs={'class': 'form-control'})
        }



class MuestraForm(ModelForm):
    """Formulario  para crear y modificar muestras.
           Se encarga de:
               * Tener una instancia del modelo muestra.
               * Agregar una muestra a la base de datos.
               * Modificar una muestra ya existente.
        :param ModelForm: Instancia de Django.forms.
        :type ModelForm: ModelForm.
       """

    class Meta:
        model = Muestra
        fields = ['nombre', 'descripcion', 'imagen']



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


class PosicionesMaquinaForm(ModelForm):
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
        fields = ['posX', 'posY', 'idLaboratorio']
        exclude = ('idMaquina',)