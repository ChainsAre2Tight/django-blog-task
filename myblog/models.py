from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    img_url = models.CharField(max_length=300, default='https://palchevsky.ru/images/blogpost.png')
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
