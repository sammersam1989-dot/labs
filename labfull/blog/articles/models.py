from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,          # обязательно указывать
        related_name="articles",           # полезно для обратных запросов
    )
    text = models.TextField()
    created_date = models.DateTimeField(   # лучшеQ DateTimeField
        auto_now_add=True,
        db_index=True,                     # ускорит сортировку/фильтрацию
    )

    class Meta:
        ordering = ["-created_date"]       # новые статьи сверху
        verbose_name = "статья"
        verbose_name_plural = "статьи"

    def __str__(self):
        return f"{self.author.username}: {self.title}"

    def get_excerpt(self):
        """Краткое содержание для списка / админки"""
        if len(self.text) > 140:
            return self.text[:137] + "..."
        return self.text
    
from django import forms
from .models import Article
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название статьи'}),
            'text': forms.Textarea(attrs={'placeholder': 'Текст статьи'}),
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if Article.objects.filter(title=title).exists():
            raise forms.ValidationError("Заголовок должен быть уникальным.")
        return title
   
class RegisterForm(UserCreationForm):
       email = forms.EmailField(required=True)

       class Meta:
           model = User
           fields = ["username", "email", "password1", "password2"]
           widgets = {
               'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
               'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
               'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
               'password2': forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}),
           }

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
