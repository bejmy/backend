from django.contrib import admin

from bejmy.labels.models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    pass
