from django.db import models
from slugify import slugify


class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name} {self.surname}"


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="book"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name="book"
    )
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Генерация slug на основе заголовка"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title