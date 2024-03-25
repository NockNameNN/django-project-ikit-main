# Generated by Django 5.0.2 on 2024-03-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('description', models.TextField(verbose_name='Описание')),
                ('featured_image', models.ImageField(blank=True, default='default.jpg', upload_to='images/')),
            ],
        ),
    ]
