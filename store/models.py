from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

   
     # to save the data
    def register(self):
        self.save()
  
    # admin site display
    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def emailExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False

class Category(models.Model):
    name = models.CharField(max_length=50)
    primaryCategory = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
  

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    inventory = models.IntegerField()
    image = models.ImageField(null=True, blank=True)
    


    def get_all_products():
        return Product.objects.all()

    def __str__(self) -> str:
        return self.name
    
    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @property
    def imageURL(self):
        try:
            url = self.iamge.url
        except:
            url = ''
        return url

  
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order \
            .objects \
            .filter(customer=customer_id)\
            .order_by('-date')
    
   
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=40)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    


