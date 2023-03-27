from django.db import models

# Create your models here.


class Product (models.Model):
    image = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text} --> {self.product.name}'
