# coding=utf-8
from django import forms
from registration.forms import RegistrationForm

from .models import IdType as IdentificationTypes, Tray
from .models import UserRole as UsrRole


class UserProfileForm(RegistrationForm):
    idTypName = IdentificationTypes.objects.all()
    usrroles = UsrRole.objects.all()

    username = forms.CharField(
        label="Nombre de Usuario",
        disabled=False
    )
    error_messages = {
        'password_mismatch': "Las contraseñas deben coincidir!",
    }
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirme su contraseña",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Repita la contraseña para verificar que sean iguales.",
    )
    userNatIdTypName = forms.ModelChoiceField(
        label="Tipo de Identificación",
        queryset=idTypName,
        empty_label="Seleccione una opción")

    userNatIdNum = forms.CharField(
        label="Número de Identificación"
    )

    userGivenName = forms.CharField(
        label="Nombres"
    )

    userLastName = forms.CharField(
        label="Apellidos"
    )

    userCode = forms.CharField(
        label="Código de Usuario",
        strip=True
    )
    userPhone = forms.CharField(
        label="Número de Teléfono"
    )
    userRoleName = forms.ModelChoiceField(
        label="Cargo",
        queryset=usrroles,
        empty_label="Seleccione una opción"
    )


class SampleRequestForm(forms.Form):


    def __init__(self, sample, *args, **kwargs):
        super(SampleRequestForm, self).__init__(*args, **kwargs)
        self.fields['id'] = forms.CharField(label="ID")
        self.fields['id'].initial=sample.id
        self.fields['name'] = forms.CharField(label="NOMBRE")
        self.fields['name'].initial=sample.name
        self.fields['description'] = forms.CharField(label="DESCRIPCION")
        self.fields['description'].initial=sample.description
        self.fields['unity'] = forms.CharField(label="UNIDAD")
        self.fields['unity'].initial = sample.unity
        self.fields['controled'] = forms.CharField(label="CONTROLADA")
        self.fields['controled'].initial=self.calc_controled(sample.controled)
        self.fields['avaliable'] = forms.CharField(label="DISPONIBLE")
        self.fields['avaliable'].initial= self.calc_disp(sample)
        self.fields['imageField'] = forms.ImageField(label="IMAGEN")
        self.fields['imageField'].initial=sample.imageField

    def calc_controled(self,controled):
        if controled==True:
            return 'Si'
        else:
            return 'No'

    def calc_disp(self,new_sample):
        trays= Tray.objects.filter(sample=new_sample)
        for tray in trays:
            if tray.empty==False:
                return 'Si'
        return 'No'