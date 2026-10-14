from django.contrib import admin

from django_project.category_app.models import CategoryModel


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(CategoryModel, CategoryAdmin)
