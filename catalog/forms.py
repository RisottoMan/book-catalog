from django import forms
from django.core.exceptions import ValidationError

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "description", "author", "genre", "quantity"]

        labels = {
            "title": "Название",
            "description": "Описание",
            "author": "Автор",
            "genre": "Жанр",
            "quantity": "Страниц"
        }

    def clean_title(self):
        """Валидация заголовка"""
        title = self.cleaned_data["title"]
        if len(title) == 0:
            raise ValidationError("Необходимо заполнить это поле")

        return title

    def clean_quantity(self):
        """Валидация количества страниц"""
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise ValidationError("Укажите положительное число")

        return quantity