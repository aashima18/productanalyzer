from django.db import models

class product(models.Model):
    product_name = models.CharField(max_length=15)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=15)
    company = models.CharField(max_length=15)
    description = models.TextField()
    def __str__(self):
        return self.product_name


class user(models.Model):
    user_name = models.CharField(max_length=20)
    contact = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    no_of_products = models.IntegerField(default=0)
    def __str__(self):
        return self.user_name



class review(models.Model):
    comment_title = models.CharField(max_length=10)
    user_name = models.ForeignKey(user , on_delete = models.CASCADE)
    contact = models.IntegerField(default=0)
    product_name = models.ForeignKey(product , on_delete = models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    post_date = models.DateField()
    def __str__(self):
        return self.comment_title


class report(models.Model):
    product_name = models.ForeignKey(product , on_delete = models.CASCADE)
    overall_rating = models.IntegerField(default=0)
    selling = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    def __str__(self):
        return self.product_name



