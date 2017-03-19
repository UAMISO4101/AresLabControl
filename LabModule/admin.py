from django.contrib import admin

from LabModule import models
from .models import UserRole, UserProfile, IdType, Sample, Project, Experiment, Protocol, Step, SampleRequest


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

class SampleAdmin(admin.ModelAdmin):


        class Meta:
            model = Sample

class ProjectAdmin(admin.ModelAdmin):
       class Meta:
           model = Project

class ExperimentAdmin(admin.ModelAdmin):
        class Meta:
            model = Experiment

class ProtocolAdmin(admin.ModelAdmin):
        class Meta:
            model = Protocol

class StepAdmin(admin.ModelAdmin):
        class Meta:
            model = Step

class RequestAdmin(admin.ModelAdmin):
        class Meta:
            model = models.Request

class SampleRequestAdmin(admin.ModelAdmin):
        class Meta:
            model = SampleRequest
# Register your models here.
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(IdType, IdTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Sample,SampleAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Experiment,ExperimentAdmin)
admin.site.register(Protocol,ProtocolAdmin)
admin.site.register(Step,StepAdmin)
admin.site.register(models.Request,RequestAdmin)
admin.site.register(SampleRequest,SampleRequestAdmin)
