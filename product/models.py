from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ('active','Active'),
        ('inactive','Inactive')
    ]

    sku = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.PositiveIntegerField()
    status = models.CharField(max_length=8,choices=STATUS_CHOICES,default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name