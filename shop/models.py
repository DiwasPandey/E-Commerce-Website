from django.db import models
from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
import math


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    image = ImageField()
    details = RichTextField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    strike_price = models.IntegerField()
    availability = models.BooleanField()
    brand = models.CharField(max_length=50)
    short_intro = RichTextField()
    sizes = models.CharField(max_length=255)
    colors = models.CharField(max_length=255)
    description = RichTextField()
    deal_of_the_day = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.title

    def image(self):
        return self.producthasimage_set.first().image

    def refined_colors(self):
        return self.colors.split(',')

    def refined_sizes(self):
        return self.sizes.split(',')

    def avg_review(self):
        out = self.producthasreview_set.aggregate(models.Avg('rating')).get('rating__avg', 0)
        return math.ceil(out if out else 0)

    def star(self):
        return range(int(self.avg_review()))

    def empty_stat(self):
        return range(5 - self.avg_review())

    def recent_reviews(self):
        return self.producthasreview_set.order_by('-id')[:3]


class ProductHasImage(models.Model):
    image = ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductHasReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def star(self):
        return range(self.rating)

    def empty_star(self):
        return range(5 - self.rating)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.IntegerField()
