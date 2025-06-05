from django.contrib import admin
from .models import Company, Genre, Platform, Game, GameGenre, GamePlatform, Review, Favorite

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_year')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'release_date', 'average_rating')
    list_filter = ('company', 'genres', 'platforms')
    search_fields = ('title',)

@admin.register(GameGenre)
class GameGenreAdmin(admin.ModelAdmin):
    list_display = ('game', 'genre')

@admin.register(GamePlatform)
class GamePlatformAdmin(admin.ModelAdmin):
    list_display = ('game', 'platform')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__username', 'game__title')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'added_at')
