from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from bejmy.users.models import User, Settings


@admin.register(User)
class UserAdmin(AuthUserAdmin):

    fieldset_extra = ('Extra', {
        'fields': (
            #'default_source_account',
            #'default_balanced',
        ),
    })

    def get_fieldsets(self, *args, **kwargs):
        fieldsets = list(super().get_fieldsets(*args, **kwargs))
        fieldsets.append(self.fieldset_extra)
        return fieldsets


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass
