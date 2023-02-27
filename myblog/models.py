from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    img_url = models.CharField(max_length=300, default='https://palchevsky.ru/images/blogpost.png')

    def __str__(self):
        return self.title
