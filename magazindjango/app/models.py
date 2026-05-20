from django.db import models
from django.contrib import admin
from datetime import datetime

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

# Регистрация в административной панели
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
