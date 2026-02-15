from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.db.models import Q

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "books/list.html"
    context_object_name = "book_list"
    paginate_by = 5
    ordering = ["-created_at"]

    def get_queryset(self):
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
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    object: Book

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_read = not self.object.is_read
        self.object.save()
        return redirect(request.path)
