from django.db import models

from django.contrib.auth.models import User


class Search(models.Model):
    squery = models.CharField(max_length=50)
    urls = models.CharField(max_length=50)
    createdat = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.squery



class Review(models.Model):
    rating = models.CharField(max_length=25, null=True, blank=True)
    no_reviews = models.CharField(max_length=50,  null=True, blank=True)
    
    star5 = models.CharField(max_length=5,  null=True, blank=True)
    star4 = models.CharField(max_length=5,  null=True, blank=True)
    star3 = models.CharField(max_length=5,  null=True, blank=True)
    star2 = models.CharField(max_length=5,  null=True, blank=True)
    star1 = models.CharField(max_length=5,  null=True, blank=True)
    
    def __str__(self):
        return self.rating


class Product(models.Model):
    rating = models.CharField(max_length=25, null=True, blank=True)
    no_reviews = models.CharField(max_length=50,  null=True, blank=True)
    star5 = models.CharField(max_length=15,  null=True, blank=True)
    star4 = models.CharField(max_length=15,  null=True, blank=True)
    star3 = models.CharField(max_length=15,  null=True, blank=True)
    star2 = models.CharField(max_length=15,  null=True, blank=True)
    star1 = models.CharField(max_length=15,  null=True, blank=True)    
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=15, null=True, blank=True)
    price = models.CharField(max_length=35, null=True, blank=True)
    url = models.CharField(max_length=15, null=True, blank=True)
    specifications = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.product_name

class Feedback(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    message=models.TextField(max_length=200)
    def __str__(self):
        return self.name