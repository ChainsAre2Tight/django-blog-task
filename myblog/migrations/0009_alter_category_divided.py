# Generated by Django 4.1.7 on 2023-02-28 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0008_category_divided_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='divided',
            field=models.BooleanField(),
        ),
    ]
