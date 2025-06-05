from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("add/", views.add_book, name="add_book"),
    path("delete/<int:book_id>/",views.delete_book, name="delete_book"),
    path("edit/<int:book_id>/", views.edit_book, name = "edit_book"),
    path("toggle-read/<int:book_id>/", views.toggle_read, name="toggle_read"),
    path("stats/", views.stats_view, name="stats"),
]
