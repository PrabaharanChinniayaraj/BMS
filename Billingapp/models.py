from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('own', 'Owner'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES,default=" ")

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    def stock_alert(self):
        if self.quantity_on_hand <= self.reorder_level:
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = "Products"
    
    
class Supplier(models.Model):
    companyname=models.CharField(max_length=100,default=" ")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def total_profit(self):
        transactions = Transaction_Sale.objects.filter(customer=self)
        total_profit = transactions.aggregate(
            total_profit=Sum(F('quantity') * (F('product__price') - F('product__buying_price')))
        )['total_profit']
        return total_profit if total_profit else 0
    
    


class Transaction_Sale(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    transcode=models.CharField(max_length=100,default="",null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.quantity_on_hand -= self.quantity 
        self.product.save()

    @property
    def total_price(self):
        return self.product.price * self.quantity
    @property
    def profit(self):
        return self.product.price - self.product.buying_price
    @property
    def total_profit(self):
        return self.profit_per_unit * self.quantity

class Transaction_Buy(models.Model):
    transaction_id = models.CharField(max_length=100, unique=False)
    transcode=models.CharField(max_length=100,default="",null=True)
    vendor = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.quantity_on_hand += self.quantity
        self.product.save()

    @property
    def total_price(self):  
        return self.product.buying_price * self.quantity