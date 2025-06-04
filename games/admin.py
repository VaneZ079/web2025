from django.contrib import admin
from .models import Company, Genre, Platform, Game, Review, Favorite

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_year')
    search_fields = ('name',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'release_date', 'average_rating')
    list_filter = ('company', 'genres', 'platforms')
    search_fields = ('title', 'company__name')
    filter_horizontal = ('genres', 'platforms')  # Удобный интерфейс для M2M полей

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'created_at')
    list_filter = ('rating', 'game')
    search_fields = ('user__username', 'game__title')
    raw_id_fields = ('user', 'game')  # Для оптимизации при большом количестве записей

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'added_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'game__title')
    raw_id_fields = ('user', 'game')