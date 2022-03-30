from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from store.middlewares.auth import auth_middleware



# Create your views here.

def homepage(request):
    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.filter(category=1)
        context = {'products': products, 'categories': categories}
        return render(request, 'store/home.html', context)

    else:
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('home')

def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
        error_message = "First name is required."
    elif len(customer.first_name) <= 2:
        error_message = "First name characters should be greater than or equal to 3."
    elif not customer.last_name:
        error_message = "Last name is Required"
    elif len(customer.last_name) <= 2:
        error_message = "Last name characters should be greater than or equal to 3."
    elif not customer.phone:
        error_message = "Phone number required."
    elif len(customer.phone) < 10:
        error_message = "Phone number should be 10 characters long"
    elif not customer.email:
        error_message = "Email is required."
    elif customer.emailExists():
        error_message = "Email is already registered."

    return error_message


def registerUser(request):
    first_name = request.POST.get("firstname")
    last_name = request.POST.get("lastname")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    password = request.POST.get("password")
    phone = request.POST.get("phone")

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'email': email
    }
    error_message = None

    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    error_message = validateCustomer(customer)

    # Validation of the fields

    if not error_message:
        customer.password = make_password(customer.password)
        customer.save()
        messages.success(request, "Registration successfully.")
        return redirect('home')
    else:
        context = {'error': error_message, 'value': value}
        return render(request, 'store/signup.html', context)


def signup(request):
    if request.method == 'GET':
        return render(request, 'store/signup.html')
    else:
        return registerUser(request)

    # return render(request, 'store/signup.html')


def login(request):
    return_url = ''
    if request.method == 'GET':
        return_url = request.GET.get('return_url')
        print(return_url)
        return render(request, 'store/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return_url = None
                    return redirect('home')
            else:
                error_message = "Email or Password is Invalid."
        else:
            error_message = "Email or Password is Invalid."
        return render(request, 'store/login.html', {'errors': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


def cart(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_product_by_id(ids)
    return render(request, 'store/cart.html', {'product': products})


def CheckOut(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))

        for product in products:
            order = Order(customer=Customer(id=customer), product=product, price=product.price, address=address,
                          phone=phone, quantity=cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}

        return redirect('cart')

    else:
        return render(request, 'store/checkout.html')

@auth_middleware
def orderView(request):
    if request.method == "GET":
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'store/orders.html', {'orders': orders})
