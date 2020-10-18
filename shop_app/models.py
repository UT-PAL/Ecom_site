from django.conf import settings
from django.db import models


# Create your models here.
class Category (models.Model):
    title = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    main_image = models.ImageField(upload_to='Products')
    name = models.CharField(max_length=264)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product',null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment',null=True)
    review = models.TextField(max_length=255)
    review_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-review_date',)

    def __str__(self):
        return self.review

class review_or_not(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review_product",null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviewer_user",null=True)

    def __str__(self):
        return self.user + " reviews " + self.product


