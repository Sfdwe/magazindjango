"""
Definition of views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import ReviewForm, NewPostForm, CommentForm
from .models import Blog, Comment
from datetime import datetime


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )
def links(request):
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )

def pool(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            
            
            category_dict = {'clothes': 'Одежда', 'shoes': 'Обувь', 'accessories': 'Аксессуары'}
            readable_category = category_dict.get(data['category'], data['category'])
            readable_subscribe = "Да" if data['subscribe'] else "Нет"
            
            
            form_data = {
                'name': data['name'],
                'email': data['email'],
                'category': readable_category,
                'score': data['score'],
                'subscribe': readable_subscribe,
                'message': data['message'],
            }
            
            return render(
                request,
                'app/pool.html',
                {
                    'title': 'Благодарим за отзыв!',
                    'form_data': form_data, 
                    'form': None,           
                    'year': datetime.now().year,
                }
            )
    else:
        form = ReviewForm()

    return render(
        request,
        'app/pool.html',
        {
            'title': 'Оставить отзыв о магазине',
            'form': form,
            'form_data': None,
            'year': datetime.now().year,
        }
    )


def registration(request):
    """Отображает страницу регистрации нового пользователя."""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST": 
        regform = UserCreationForm(request.POST)
        if regform.is_valid(): 
            reg_f = regform.save(commit=False) 
            reg_f.is_staff = False 
            reg_f.is_active = True 
            reg_f.is_superuser = False 
            reg_f.date_joined = datetime.now() 
            reg_f.last_login = datetime.now() 
            
            reg_f.save() 
            return redirect('home') 
    else:
        regform = UserCreationForm() 

    return render(
        request,
        'app/registration.html',
        {
            'title': 'Регистрация',
            'regform': regform,
            'year': datetime.now().year,
        }
    )
from .models import Blog
from django.http import HttpRequest

def blog(request):
    """Отображает страницу со списком всех статей (ленту)."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # Выборка всех статей
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог о моде',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Отображает страницу конкретной статьи по её ID."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # Выборка статьи по параметру ID
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'year': datetime.now().year,
        }
    )
def newpost(request):
    """Добавление статьи администратором."""
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            Blog.objects.create(
                title=form.cleaned_data['title'],
                short_description=form.cleaned_data['short_description'],
                content=form.cleaned_data['content'],
                image=form.cleaned_data['image']
            )
            return redirect('blog')
    else:
        form = NewPostForm()
    return render(request, 'app/newpost.html', {'title': 'Добавить статью', 'form': form, 'year': datetime.now().year})

def videopost(request):
    """Отображение страницы с видео."""
    return render(request, 'app/videopost.html', {'title': 'Видео-презентации', 'year': datetime.now().year})
def blogpost(request, parametr):
    """Отображает страницу конкретной статьи по ID и обрабатывает комментарии."""
    assert isinstance(request, HttpRequest)
    
    post_1 = get_object_or_404(Blog, id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

