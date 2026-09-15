from django.db import models
from django.contrib import admin
from datetime import datetime

# ================= БЛОК БЛОГА И КОММЕНТАРИЕВ (ОСТАВЛЯЕМ) =================

class Blog(models.Model):
    """Модель статьи для раздела новостей и стиля магазина FashionShop."""
    title = models.CharField(max_length=100, unique=True, verbose_name="Заголовок статьи")
    short_description = models.CharField(max_length=255, verbose_name="Краткое содержание статьи")
    content = models.TextField(verbose_name="Полное содержание статьи")
    image = models.ImageField(upload_to="media/", verbose_name="Картинка к статье", blank=True, null=True)
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")

    class Meta:
        ordering = ['-posted']
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"

    def __str__(self):
        return self.title

admin.site.register(Blog)


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name="Статья")
    author = models.CharField(max_length=100, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликован")

    class Meta:
        ordering = ['-posted']
        verbose_name = "Комментарий блога"
        verbose_name_plural = "Комментарии блога"

    def __str__(self):
        return f"Комментарий от {self.author} к {self.post.title}"

admin.site.register(Comment)




class Category(models.Model):
    """Модель категории каталога (Пункт 1 ТЗ)."""
    title = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории", blank=True)

    class Meta:
        verbose_name = "Категория каталога"
        verbose_name_plural = "Категории каталога"

    def __str__(self):
        return self.title

admin.site.register(Category)


class Product(models.Model):
    """Модель элемента каталога (товара/услуги) (Пункт 1 ТЗ)."""
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products', 
        verbose_name="Категория (внешний ключ)"
    )
    title = models.CharField(max_length=100, verbose_name="Название товара")
    short_description = models.CharField(max_length=255, verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image_url = models.URLField(max_length=500, verbose_name="Ссылка на картинку", blank=True)
    posted = models.DateTimeField(default=datetime.now, verbose_name="Добавлен в каталог")

    class Meta:
        ordering = ['-posted']
        verbose_name = "Элемент каталога"
        verbose_name_plural = "Элементы каталога"

    def __str__(self):
        return f"{self.title} ({self.category.title})"

admin.site.register(Product)
