from django.contrib import admin

from .models import UserRole, UserProfile, IdType, Sample


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

# Register your models here.
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(IdType, IdTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Sample,SampleAdmin)
