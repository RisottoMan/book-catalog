from django.urls import path
from . import views


urlpatterns = [
    # Book представления
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<slug:slug>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book_delete'),

    # Author представления
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]