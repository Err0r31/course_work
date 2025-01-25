from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords

class Priority(models.Model):
    level = models.CharField(max_length=50, verbose_name="Уровень приоритета")
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        validators=[RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'Некорректный формат цвета')],
        verbose_name="Цвет приоритета"
    )

    def __str__(self):
        return self.level


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        validators=[RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'Некорректный формат цвета')],
        verbose_name="Цвет приоритета"
    )

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        validators=[RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'Некорректный формат цвета')],
        verbose_name="Цвет приоритета"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='tasks')
    title = models.CharField(max_length=150, verbose_name="Заголовок задачи")
    description = models.TextField(verbose_name="Описание задачи", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Срок выполнения", db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_completed = models.BooleanField(default=False, verbose_name="Завершено")
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, verbose_name="Приоритет")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги", related_name='tasks')

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self.is_completed = True
        else:
            self.is_completed = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Задача", related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания комментария")

    def __str__(self):
        return f"Комментарий от {self.user.username} для задачи {self.task.title}"


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return f"Вложение для задачи {self.task.title}"
