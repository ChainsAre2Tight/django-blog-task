from django.db import models
from django.utils.text import slugify
from transliterate import translit
from datetime import datetime


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()
    divided = models.BooleanField()
    img_url = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(null=True, max_length=40, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    img_url = models.CharField(max_length=300, blank=True)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Image(models.Model):
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', default=None)
