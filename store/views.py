from django.shortcuts import render
from .models import Product, Customer
from django.http import HttpResponse
from multiprocessing import context

# Create your views here.
def index(request):
    customer = Customer.objects.all()
    product = product.objects.all()

    return render(request,'store/main.html',{'products':list(product),'customers':list(customer)})