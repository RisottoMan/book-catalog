from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Author, Book
from .forms import BookForm


class BookListView(ListView):
    """Представление для просмотра списка книг"""
    model = Book
    template_name = "book/list.html"
    context_object_name = "book_list"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
        """Формирование запроса по GET-параметрам"""
        queryset = super().get_queryset().select_related('genre', 'author')
        filters = Q()

        genre_slug = self.request.GET.get('genre')
        if genre_slug:
            filters &= Q(genre__slug=genre_slug)

        author_id = self.request.GET.get('author')
        if author_id:
            filters &= Q(author__id=author_id)

        read_param = self.request.GET.get('read')
        if read_param:
            read_param = read_param.lower()
            if read_param in ["true", "false"]:
                is_read = read_param == "true"
                filters &= Q(is_read=is_read)

        return queryset.filter(filters)


class BookDetailView(DetailView):
    """Представление для просмотра одной книги"""
    model = Book
    template_name = "book/detail.html"
    context_object_name = "book"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    object: Book

    def post(self, request, *args, **kwargs):
        """Меняем статус книги после нажатия на кнопку"""
        self.object = self.get_object()
        self.object.is_read = not self.object.is_read
        self.object.save()
        return redirect(request.path)


class BookCreateView(CreateView):
    """Представление для создания книги"""
    model = Book
    form_class = BookForm
    template_name = "book/create.html"

    def get_success_url(self):
        """Перенаправление после успешного сохранения"""
        return reverse_lazy("book_detail", kwargs={"slug": self.object.slug})


class BookUpdateView(UpdateView):
    """Представление для обновления книги"""
    model = Book
    form_class = BookForm
    template_name = "book/update.html"

    def get_success_url(self):
        """Перенаправление после успешного сохранения"""
        return reverse_lazy("book_detail", kwargs={"slug": self.object.slug})


class BookDeleteView(DeleteView):
    """Представление для удаления книги"""
    model = Book
    template_name = "book/delete.html"
    success_url = reverse_lazy("book_list")


class AuthorDetailView(DetailView):
    """Представление для просмотра автора и всех его книг"""
    model = Author
    template_name = "author/detail.html"
    context_object_name = "author"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        """Формирование дополнительных полей в шаблон"""
        context = super().get_context_data(**kwargs)
        author = context["author"]

        author.full_name = f"{author.name} {author.surname}"
        context["book_list"] = Book.objects.filter(author=author)

        return context