from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="store/images/")

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=400)
    payment_data = models.TextField(null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    item = models.TextField(null=True)
    fullfilled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
