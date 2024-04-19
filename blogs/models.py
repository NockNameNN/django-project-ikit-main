from django.db import models
from django.urls import reverse
from transliterate import slugify


class SlugBase(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(SlugBase):
    pass


class Tag(SlugBase):
    pass


class Comment(models.Model):
    body = models.CharField(max_length=500)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.body} - написал {self.author}'


class Post(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT, default=1)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги", blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=0, verbose_name="Категория")
    featured_image = models.ImageField(blank=True, default="default.jpg", upload_to="images/")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"category": self.category.slug, "slug": self.slug})

    def __str__(self):
        return f"{self.name}"




