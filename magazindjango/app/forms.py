from django import forms
from django.contrib.auth.forms import AuthenticationForm


class BootstrapAuthenticationForm(AuthenticationForm):
    """Форма авторизации, использующая стили Bootstrap."""
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))



class ReviewForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    CATEGORY_CHOICES = [
        ('clothes', 'Одежда'),
        ('shoes', 'Обувь'),
        ('accessories', 'Аксессуары'),
    ]
    category = forms.ChoiceField(
        label="Что вы покупали?",
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    SCORE_CHOICES = [
        ('1', '1 - Плохо'),
        ('2', '2 - Посредственно'),
        ('3', '3 - Удовлетворительно'),
        ('4', '4 - Хорошо'),
        ('5', '5 - Отлично'),
    ]
    score = forms.ChoiceField(
        label="Оцените качество обслуживания:",
        choices=SCORE_CHOICES,
        widget=forms.RadioSelect
    )
    
    subscribe = forms.BooleanField(
        label="Хочу получать информацию о скидках и закрытых распродажах",
        required=False
    )
    
    message = forms.CharField(
        label="Текст вашего отзыва",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        min_length=10,
        max_length=1000
    )
class NewPostForm(forms.Form):
    title = forms.CharField(label="Заголовок статьи", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_description = forms.CharField(label="Краткое содержание", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Полное содержание", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    image = forms.ImageField(label="Изображение для статьи", required=False)
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Напишите комментарий...'}),
        }
from .models import Product

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'short_description', 'full_description', 'price', 'image_url')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Краткое описание'}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Полное описание'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ссылка на картинку'}),
        }
from .models import Category

class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание категории'}),
        }
