# Generated by Django 4.1.7 on 2023-03-07 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0013_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
    ]
