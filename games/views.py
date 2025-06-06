from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Avg
from .models import Game, Genre, Platform, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .forms import GameForm



@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review.rating = rating
        review.comment = comment
        review.save()
        return redirect('game_detail', game_id=review.game.id)

    return redirect('game_detail', game_id=review.game.id)

def ed_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':
        game.title = request.POST.get('title')
        game.description = request.POST.get('description')
        # Обновляем другие поля по необходимости
        game.save()
        return redirect('game_detail', game_id=game.id)
    
    return redirect('game_detail', game_id=game.id)

def home(request):
    games = Game.objects.all()
    genres = Genre.objects.all()
    platforms = Platform.objects.all()

    q = request.GET.get('q', '')
    genre_id = request.GET.get('genre')
    platform_id = request.GET.get('platform')

    if q:
        games = games.filter(title__icontains=q)

    if genre_id:
        games = games.filter(genres__id=genre_id)

    if platform_id:
        games = games.filter(platforms__id=platform_id)

    games = games.distinct()

    top_games = Game.objects.annotate(
        review_count=Count('review'),
        avg_rating=Avg('review__rating')
    ).filter(
        review__created_at__gte=timezone.now() - timedelta(days=30),
        review_count__gte=1
    ).order_by('-avg_rating')[:5]

    recent_reviews = Review.objects.select_related('user', 'game').order_by('-created_at')[:5]

    context = {
        'games': games,
        'genres': genres,
        'platforms': platforms,
        'top_games': top_games,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'games/home.html', context)
    


@login_required
def add_review(request, game_id):
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        if 0 <= rating <= 5 and comment:
            Review.objects.create(
                user=request.user,
                game_id=game_id,
                rating=rating,
                comment=comment,
            )
        return redirect('game_detail', game_id=game_id)
    return redirect('game_detail', game_id=game_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        game_id = review.game.id
        review.delete()
        return redirect('game_detail', game_id)
    return redirect('game_detail', review.game.id)

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'games/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'games/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def favorites(request):
    # Пока пустой пример
    favorite_games = []
    return render(request, 'games/favorites.html', {'games': favorite_games})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'games/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'games/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    reviews = Review.objects.filter(game=game).order_by('-created_at')
    edit_review_id = request.GET.get('edit')
    edit_game = request.GET.get('edit_game') == 'true'

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    form = None
    if request.method == 'POST' and edit_game and request.user.is_authenticated:
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            updated_game = form.save(commit=False)
            updated_game.save() 
            form.save_m2m() 
            return redirect('game_detail', game_id=game.id)
        else:
            print(form.errors)
    elif edit_game and request.user.is_authenticated:
        form = GameForm(instance=game)

    context = {
        'game': game,
        'reviews': reviews,
        'edit_review_id': int(edit_review_id) if edit_review_id and edit_review_id.isdigit() else None,
        'user_review': user_review,
        'edit_game': edit_game,
        'form': form,
    }

    return render(request, 'games/game_detail.html', context)



def favorites(request):
    return render(request, 'games/favorites.html')


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=150)
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput,
        help_text='',  # Убираем подсказки
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput,
        help_text='',
    )

    class Meta:
        model = User
        fields = ("username",)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную
    else:
        form = CustomUserCreationForm()
    return render(request, 'games/register.html', {'form': form})

