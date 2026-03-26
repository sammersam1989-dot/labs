from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article
from django.contrib.auth.models import User

def archive(request):
    query = request.GET.get('q')
    posts_list = Article.objects.all().order_by('-created_date')
    if query:
        posts_list = posts_list.filter(Q(title__icontains=query) | Q(text__icontains=query))
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'archive.html', {'posts': posts, 'query': query})

def get_article(request, article_id):
    post = get_object_or_404(Article, id=article_id)
    return render(request, 'article.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:
            if Article.objects.filter(title=title).exists():
                messages.error(request, 'Статья с таким названием уже существует')
                return render(request, 'create_post.html', {'title': title, 'text': text})
            article = Article.objects.create(title=title, text=text, author=request.user)
            messages.success(request, 'Статья создана!')
            return redirect('get_article', article_id=article.id)
        else:
            messages.error(request, 'Заполните оба поля')
            return render(request, 'create_post.html', {'title': title, 'text': text})
    return render(request, 'create_post.html')

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user != article.author and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав на редактирование')
        return redirect('get_article', article_id=article.id)
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:
            if Article.objects.filter(title=title).exclude(id=article.id).exists():
                messages.error(request, 'Статья с таким названием уже существует')
                return render(request, 'edit_article.html', {'post': article})
            article.title = title
            article.text = text
            article.save()
            messages.success(request, 'Статья обновлена')
            return redirect('get_article', article_id=article.id)
        else:
            messages.error(request, 'Заполните оба поля')
    return render(request, 'edit_article.html', {'post': article})

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user != article.author and not request.user.is_superuser:
        messages.error(request, 'У вас нет прав на удаление')
        return redirect('get_article', article_id=article.id)
    article.delete()
    messages.success(request, 'Статья удалена')
    return redirect('archive')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not username or not password:
            messages.error(request, 'Имя пользователя и пароль обязательны')
            return render(request, 'register.html')
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('archive')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('archive')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('archive')