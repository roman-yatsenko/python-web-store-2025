from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', 
                                 on_delete=models.CASCADE, verbose_name='Категорія')
    name = models.CharField(max_length=300, verbose_name='Назва')
    slug = models.SlugField(max_length=300)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, 
                              verbose_name='Зоюраження')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    available = models.BooleanField(default=True, verbose_name='В наявності')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Додано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Змінено')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
