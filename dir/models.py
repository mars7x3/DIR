from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    slug = models.SlugField(primary_key=True, verbose_name='Слаг')
    parent = models.ForeignKey('self',
                               on_delete=models.DO_NOTHING,
                               related_name='children',
                               blank=True, null=True,
                               verbose_name='Родительская категория')

    def __str__(self):
        if self.parent:
            return f'{self.parent} | {self.name}'
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Resume(models.Model):
    STATUS_RESUME = (
        ('Найти работника', 'Найти работника'),
        ('Найти работу', 'Найти работу'),
    )
    status = models.CharField(choices=STATUS_RESUME,
                              max_length=30,
                              default='Активна',
                              verbose_name='Статус')

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='user',
                                verbose_name='Пользователь')
    name = models.CharField(max_length=100, )
    phone = models.CharField(max_length=100, )
    title = models.CharField(max_length=300, )
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING,
                                 related_name='resume')
    description = models.TextField()
    price = models.PositiveIntegerField()
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Время создания')

    image = models.ImageField(upload_to='products',
                              verbose_name='Изображение',)
    address = models.CharField(max_length=300, )

    def get_absolut_url(self):
        from django.urls import reverse
        return reverse('resume', kwargs={'resume_id': self.id})


class Review(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resumes')
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 related_name='author',
                                 verbose_name='Пользователь',
                                 blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING,
                               related_name='replies',
                               blank=True, null=True)



