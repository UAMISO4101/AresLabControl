# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm
from .forms import UserCreationForm
from .models import AccountProfile
from .models import AccountRole
from .models import ActivationProfile
from .models import DocumentIDType
from .models import Experimento
from .models import LabUser
from .models import LaboratorioProfile
from .models import MaquinaEnLab
from .models import MaquinaProfile
from .models import Muestra
from .models import MuestraSolicitud
from .models import Paso
from .models import Projecto
from .models import Protocolo
from .models import Solicitud


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'user_code', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'user_code', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_phone',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Access', {'fields': ('is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'email', 'user_code',)
    ordering = ('username', 'email', 'user_code',)
    filter_horizontal = ()


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["__unicode__"]

    class Meta:
        model = AccountRole


class IdTypeAdmin(admin.ModelAdmin):
    class Meta:
        model = DocumentIDType


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "user", "userRole"]

    class Meta:
        model = AccountProfile


# Register your models here.
admin.site.register(LabUser, UserAdmin)
admin.site.register(AccountRole, UserRoleAdmin)
admin.site.register(DocumentIDType, IdTypeAdmin)
admin.site.register(AccountProfile, UserProfileAdmin)
admin.site.register(ActivationProfile)
admin.site.register(MaquinaProfile)
admin.site.register(Muestra)
admin.site.register(Projecto)
admin.site.register(Experimento)
admin.site.register(Protocolo)
admin.site.register(Paso)
admin.site.register(Solicitud)
admin.site.register(MuestraSolicitud)
admin.site.register(LaboratorioProfile)
admin.site.register(MaquinaEnLab)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
