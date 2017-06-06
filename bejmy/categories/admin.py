from django.contrib import admin

from bejmy.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
