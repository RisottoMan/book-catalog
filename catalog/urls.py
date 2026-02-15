from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/create/', '', name='book_create'),
    path('books/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<slug:slug>/update/', '', name='book_update'),
    path('books/<slug:slug>/delete/', '', name='book_delete'),

    path('authors/<slug:slug>/', '', name='author_detail'),
]