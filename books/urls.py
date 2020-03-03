from django.urls import path
from books import views

urlpatterns = [
    path('upload/', views.CreateBookView.as_view(), name='create_book'),
    path('<int:pk>/', views.DetailBook.as_view(), name='detail_book'),
    path('<str:genre>/', views.BookGenreView.as_view(), name='genre_book'),
    # path('<int:pk>/update/', views.BookUpdateView.as_view(), name='update_book'),
    path('<int:pk>/update/', views.post_update, name='update_book'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete_book'),
]
