"""
Definition of views.
"""

from .models import Blog, Comment, Category, Product
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .forms import ReviewForm, NewPostForm, CommentForm, NewProductForm, NewCategoryForm




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

# ================= КОД ДЛЯ БЛОГА (ВОЗВРАЩАЕМ КАК БЫЛО) =================

def blog(request):
    """Отображает страницу новостей/блога."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()  # Возвращаем выборку старых статей блога
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Отображает детальную страницу статьи блога (старый вариант)."""
    assert isinstance(request, HttpRequest)
    post_1 = get_object_or_404(Blog, id=parametr)
    comments = Comment.objects.filter(post=post_1)  # Комментарии к статье блога

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


# ================= НОВЫЙ КОД ДЛЯ КАТАЛОГА ПО ТЗ =================

def catalog(request):
    """Отображает главную страницу каталога с категориями (Пункт 2 и 3 ТЗ)."""
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=current_category)
    else:
        current_category = None
        products = Product.objects.all()

    return render(
        request,
        'app/catalog.html',  # Сделаем для каталога отдельный HTML-файл!
        {
            'title': 'Каталог товаров',
            'categories': categories,
            'current_category': current_category,
            'products': products,
            'year': datetime.now().year,
        }
    )

def product_detail(request, parametr):
    """Отображает карточку конкретного товара (Пункт 4 ТЗ)."""
    assert isinstance(request, HttpRequest)
    product = get_object_or_404(Product, id=parametr)
    
    # Чтобы не путать с комментариями блога, отзывы к товарам можно выводить так:
    # (Для простоты пока оставим форму CommentForm, но привяжем к product в будущем)
    return render(
        request,
        'app/product_detail.html',  # Отдельный HTML для карточки товара!
        {
            'product': product,
            'year': datetime.now().year,
        }
    )
def newpost(request):
    """Добавление товаров администратором с сайта (Пункт 5 ТЗ)."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_superuser:  # Проверка прав администратора
        return redirect('home')
    
    if request.method == "POST":
        form = NewProductForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем товар в базу данных
            return redirect('catalog')  # Перенаправляем на страницу каталога
    else:
        form = NewProductForm()
        
    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Добавить товар в каталог',
            'form': form,
            'year': datetime.now().year,
        }
    )
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
def newcategory(request):
    """Добавление новых категорий администратором с сайта (Пункт 5 ТЗ)."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == "POST":
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog') # Перенаправляем в каталог после добавления
    else:
        form = NewCategoryForm()
        
    return render(
        request,
        'app/newcategory.html',
        {
            'title': 'Добавить категорию в каталог',
            'form': form,
            'year': datetime.now().year,
        }
    )

