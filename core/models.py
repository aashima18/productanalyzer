from django.db import models

from django.contrib.auth.models import User


class Search(models.Model):
    squery = models.CharField(max_length=50)
    urls = models.CharField(max_length=50)
    createdat = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.squery






class Product(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=15, null=True, blank=True)
    price = models.CharField(max_length=35, null=True, blank=True)
    category = models.CharField(max_length=15, null=True, blank=True)
    specifications = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.product_name




class review(models.Model):
    comment_title = models.CharField(max_length=10)
    user_name = models.ForeignKey(User , on_delete = models.CASCADE)
    product_name = models.ForeignKey(Product , on_delete = models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    reviews = models.CharField(max_length=50)
    post_date = models.DateField()
    def __str__(self):
        return self.comment_title



