# Generated by Django 5.0.3 on 2024-05-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default='postzzz'),
        ),
    ]
