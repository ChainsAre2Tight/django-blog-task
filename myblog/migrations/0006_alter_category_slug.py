# Generated by Django 4.1.7 on 2023-02-28 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=50), max_length=40, null=True, unique=True),
        ),
    ]