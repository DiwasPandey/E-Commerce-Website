from django.db import models
from sorl.thumbnail import ImageField
from ckeditor.fields import RichTextField


# Create your models here.

class TopBanner(models.Model):
    image = ImageField()
    title_text = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, blank=True)
    button_text = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.title_text


class BottomBanner(models.Model):
    image = ImageField()
    is_big = models.BooleanField()
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, blank=True)
    button_text = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(max_length=50)
    weight = models.IntegerField()
    href = models.CharField(max_length=255)

    def __str__(self):
        return self.title
