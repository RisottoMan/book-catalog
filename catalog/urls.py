from django.urls import path
from . import views


urlpatterns = [
    # Book представления
    path('book/', views.BookListView.as_view(), name='book_list'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create'),
    path('book/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<slug:slug>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('book/<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book_delete'),

    # Author представления
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]