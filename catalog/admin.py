from django.contrib import admin
from .models import Author, Genre, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели Author"""
    list_display = ('full_name', 'name', 'surname', 'birth_date')
    search_fields = ['name', 'surname']

    @admin.display(description="Full Name")
    def full_name(self, obj):
        return f"{obj.name} {obj.surname}"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели Genre"""
    list_display = ('name', 'slug')
    search_fields = ['name', 'slug']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели Book"""
    list_display = ('full_title', 'slug', 'title', 'author', 'genre', 'quantity', 'is_read')
    search_fields = ['title', 'slug', 'author__name', 'author__surname', 'genre__name', 'is_read']

    @admin.display(description="Full Title")
    def full_title(self, obj):
        return f"«{obj.title}» {obj.author}"