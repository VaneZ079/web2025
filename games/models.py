from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField("Название компании", max_length=100, unique=True)
    country = models.CharField("Страна", max_length=100)
    founded_year = models.IntegerField("Год основания")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=50, unique=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField("Название платформы", max_length=50, unique=True)
    release_year = models.IntegerField("Год выхода")

    class Meta:
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField("Название игры", max_length=200)
    description = models.TextField("Описание игры")
    release_date = models.DateField("Дата выхода")
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания-разработчик"
    )

    cover_image = models.ImageField("Обложка", upload_to='game_images/covers/')
    detail_image = models.ImageField(
        "Детальное изображение",
        upload_to='game_images/details/'
    )

    average_rating = models.FloatField("Средний рейтинг", default=0.0)

    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    platforms = models.ManyToManyField(Platform, verbose_name="Платформы")

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name="Игра"
    )
    rating = models.IntegerField("Оценка", choices=RATING_CHOICES)
    comment = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name="Игра"
    )
    added_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"