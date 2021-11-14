from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)  # SlugField - текстовое поле. Url должен быть уникальным

    def __str__(self):  # Возвращает строковое представление нашей модели
        return self.name

    class Meta:  # Контейнер с данными
        verbose_name = "Категория"  # Имя для объекта в единственном числе
        verbose_name_plural = "Категории"  # Имя для объекта во множественном числе


class Actor(models.Model):
    """Актёры и режиссеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models. TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")   # Upload_to="actors/" - указываем дирректорию
    # куда будем загружать изображение.

    def __str__(self):
        return self.name

    class Meta:  # Контейнер с данными
        verbose_name = "Актеры и режиссеры"  # Имя для объекта в единственном числе
        verbose_name_plural = "Актеры и режиссеры"  # Имя для объекта во множественном числе


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models. TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:  # Контейнер с данными
        verbose_name = "Жанр"  # Имя для объекта в единственном числе
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильм"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", default="", max_length=100)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")  # verbose_name
    # - имя для поля, related_name - имя использованное для отношения связи объекта
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указать сумму в долларах")  # help_text -
    # вспомогательный текст для поля формы
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="указать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="указать сумму в долларах")
    category = models.ForeignKey(Category, verbose_name="категория", on_delete=models.SET_NULL, null=True)  #
    # on_delete=models.SET_NULL - Если удалим категорию, то данное поле будет NULL
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # метод который возвращает ссылку
        return reverse('movie_detail', kwargs={"slug": self.url})

    class Meta:  # Контейнер с данными
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:  # Контейнер с данными
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:  # Контейнер с данными
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="Звезда", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:  # Контейнер с данными
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, null=True, blank=True)
    # "self" - запись ссылается на запись в этой же таблице
    # blank=True - Поле НЕ обязательно для заполнения
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:  # Контейнер с данными
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


