from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie  # метод get принимает запросы http. В request содержится вся информация присланная от
    # клиента
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """Полное описания фильма"""
    model = Movie
    slug_field = 'url'  # поле по которому мы будем искать нашу запись (по полю url)
    # Мы не писали template_name потому что он автоматически находит наш шаблон, так как мы используем DetailView,
    # то джанго автоматически берет имя модели и добавляет _detail --> получается имя шаблона.


