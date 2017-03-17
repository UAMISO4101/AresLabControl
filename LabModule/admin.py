from django.contrib import admin

from .models import UserRole, UserProfile, IdType,MaquinaProfile


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
