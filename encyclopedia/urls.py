from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("<str:name>", views.entry, name="entry"),
    path("random/", views.randompage, name="randompage"),
    path("<str:name>/editpage", views.editpage, name="editpage")
]
