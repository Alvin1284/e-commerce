from django.db import models


# Create your models here.


class Customer(models.Model):
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

  
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    ordered = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=250, blank=True, null=True )
    
   
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

    


