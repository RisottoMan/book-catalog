from datetime import date
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from .models import Author, Book, Genre
from .forms import BookForm


# forms.py
class BookFormTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='Name',
            surname='Surname',
            birth_date=date(1990, 1, 1)
        )
        self.genre = Genre.objects.create(
            name='Genre',
            slug='genre'
        )

    def test_valid_form(self):
        data = {
            'title': 'Title',
            'description': 'Description',
            'author': self.author.id,
            'genre': self.genre.id,
            'quantity': 100
        }
        form = BookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_empty_title(self):
        data = {
            'title': '',
            'description': 'Description',
            'author': self.author.id,
            'genre': self.genre.id,
            'quantity': 100
        }
        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_zero_quantity(self):
        data = {
            'title': 'Title',
            'description': 'Description',
            'author': self.author.id,
            'genre': self.genre.id,
            'quantity': 0
        }
        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_negative_quantity(self):
        data = {
            'title': 'Title',
            'description': 'Description',
            'author': self.author.id,
            'genre': self.genre.id,
            'quantity': -10
        }
        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)


# views.py
class BookViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Добавление авторов
        cls.author1 = Author.objects.create(name='Стивен', surname='Кинг')
        cls.author2 = Author.objects.create(name='Лев', surname='Толстой')
        cls.author3 = Author.objects.create(name='Александр', surname='Пушкин')

        # Добавление жанров
        cls.genre1 = Genre.objects.create(name='Фантастика', slug='fantasy')
        cls.genre2 = Genre.objects.create(name='Роман', slug='novel')
        cls.genre3 = Genre.objects.create(name='Поэма', slug='poem')

        # Добавление книг
        cls.book1 = Book.objects.create(
            title='Туман',
            description='Description',
            author=cls.author1,
            genre=cls.genre1,
            quantity=100,
        )
        cls.book2 = Book.objects.create(
            title='Война и Мир',
            description='Description',
            author=cls.author2,
            genre=cls.genre2,
            quantity=1000,
            is_read=True,
        )
        cls.book3 = Book.objects.create(
            title='Руслан и Людмила',
            description='Description',
            author=cls.author3,
            genre=cls.genre3,
            quantity=250,
        )
        cls.book4 = Book.objects.create(
            title='Сияние',
            description='Description',
            author=cls.author1,
            genre=cls.genre1,
            quantity=370,
            is_read=True,
        )
        cls.book5 = Book.objects.create(
            title='Оно',
            description='Description',
            author=cls.author1,
            genre=cls.genre1,
            quantity=560,
            is_read=True,
        )
        cls.book6 = Book.objects.create(
            title='Дубровский',
            description='Description',
            author=cls.author3,
            genre=cls.genre2,
            quantity=250,
        )

    def test_first_page(self):
        """Проверка без фильтра с учётом пагинации"""
        url = reverse_lazy('books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 5)

    def test_filter_by_genre(self):
        """Проверка фильтра по жанру"""
        url = reverse_lazy('books')
        response = self.client.get(url, {'genre': self.genre2.slug})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 2)

    def test_filter_by_author(self):
        """Проверка фильтра по автору"""
        url = reverse_lazy('books')
        response = self.client.get(url, {'author': self.author3.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 2)

    def test_filter_by_read(self):
        """Проверка фильтра по полю 'Прочитано'"""
        url = reverse_lazy('books')
        response = self.client.get(url, {'read': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 3)

    def test_filter_by_multiple_params(self):
        """Проверка комбинированных фильтров"""
        url = reverse_lazy('books')
        response = self.client.get(url, {
            'author': self.author1.id,
            'genre': self.genre1.slug,
            'read': False,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 1)

    def test_change_is_read_status(self):
        """Изменение статуса is_read через POST"""
        initial_read_value = self.book1.is_read

        # Переходим по slug в URL
        url = reverse_lazy('book_detail', kwargs={'slug': self.book1.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # Проверяем статус записи
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.is_read, initial_read_value)

    def test_book_create(self):
        """Проверка создания новой книги через POST"""
        url = reverse_lazy('book_create')
        data = {
            'title': 'Test',
            'description': 'Description',
            'author': self.author3.id,
            'genre': self.genre3.id,
            'quantity': 10
        }

        response = self.client.post(url, data)

        # Проверка кастомных полей записи
        book = Book.objects.get(title='Test')
        self.assertIsNotNone(book.slug)

        # Проверка перехода на страницу книги
        expected_url = reverse('book_detail', kwargs={'slug': book.slug})
        self.assertRedirects(response, expected_url)