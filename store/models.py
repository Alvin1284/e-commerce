import datetime
from unicodedata import category
from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class meta:
        db_table = 'store_customer'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]

     # to save the data
    def register(self):
        self.save()
  
    # search customer by email
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
  
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
  
        return False

    def __str__(self) -> str:
        return self.first_name

class Category(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.name
  

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    inventory = models.IntegerField()

    def get_all_products():
        return Product.objects.all()

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)