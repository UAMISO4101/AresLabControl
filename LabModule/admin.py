from django.contrib import admin

from LabModule import models
from .models import UserRole, UserProfile, IdType,MaquinaProfile, Sample, Experiment, Project, Protocol, Step, \
    SampleRequest


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["__unicode__"]

    class Meta:
        model = UserRole


class IdTypeAdmin(admin.ModelAdmin):
    class Meta:
        model = IdType


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "userCode", "user", "userRole"]

    class Meta:
        model = UserProfile


# Register your models here.
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(IdType, IdTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MaquinaProfile)
admin.site.register(Sample)
admin.site.register(Project)
admin.site.register(Experiment)
admin.site.register(Protocol)
admin.site.register(Step)
admin.site.register(models.Request)
admin.site.register(SampleRequest)