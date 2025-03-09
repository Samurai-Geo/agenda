from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# id (primary key - automático criado pelo Django)
# first_name (string), last_name (string), phone (string)
# email (email), created_date (date), description (text)
# category (foreign key), show (boolean), owner (foreign key)
# picture (image)

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'

class Contact(models.Model):
    class Meta:
     verbose_name = 'Contact'
     verbose_name_plural = 'Contacts'

    first_name = models.CharField(max_length=50, verbose_name='Nome')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Sobrenome')
    phone = models.CharField(max_length=12, verbose_name='Telefone')
    email = models.EmailField(max_length=254, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, verbose_name='Descrição')
    show = models.BooleanField(default=True, verbose_name='mostrar')
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m', verbose_name='Foto')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Categorai',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'