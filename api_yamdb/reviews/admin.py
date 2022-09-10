from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title


@admin.register(Category, Genre, GenreTitle, Title)
class PersonAdmin(admin.ModelAdmin):
    pass
