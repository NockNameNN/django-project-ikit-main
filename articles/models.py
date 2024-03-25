from django.db import models

# Create your models here.

class Article(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    characters = models.IntegerField(verbose_name="Количество страниц")
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")

    def __str__(self):
        return f"{self.name}"
