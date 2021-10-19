import uuid
import requests
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Category,Product,ShopCart, Payment
from django.contrib import messages
from . forms import RegistrationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# import requests
import json
# Create your views here.


def index(request):
    categories = Category.objects.all()[:3]
    bseller = Product.objects.filter(best_seller=True,avaliable=True)
    latest = Product.objects.filter(latest=True,avaliable=True)

    context = {
        'categories': categories,
        'bseller':bseller,
        'latest':latest
    }

    return render(request, 'index.html',context)



def categories(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }
    return render(request, 'categories.html',context)



def products(request):
    products = Product.objects.all().filter(avaliable=True)
    categories = Category.objects.all()

    context={
        'products':products,
        'categories':categories
    }


    return render(request, 'products.html',context)

def category(request,id):
    category = Product.objects.filter(category_id=id)

    context = {
        'category':category
    }

    return render(request, 'category.html',context)


def product(request,id):
    product = Product.objects.get(pk=id)

    context = {
        'product':product
    }

    return render(request, 'products.html',context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, 'login successful')
            return redirect('index')
        else:
            messages.success(request, 'username/password incorrect')
            return redirect('loginpage')

    return render(request, 'loginpage.html')


def logoutpage(request):
    logout(request)
    messages.success(request, 'logout successful')
    return redirect('loginpage')
    


def registerpage(request):
    regform = RegistrationForm()
    if request.method == 'POST':
        regform = RegistrationForm(request.POST)
        if regform.is_valid():
            messages.success(request, 'signup successful')
            return redirect('index')
        else:
            messages.warning(request, regform.errors)
            return redirect('registerpage')

    context ={
        'regform':regform
    }
    return render(request, 'registerpage.html',context)

def password(request):
    update = PasswordChangeForm(request.user)
    if request.method == 'POST':
        update = PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user = update.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'password update successful')
            return redirect('index')
        else:
            messages.error(request, update.errors)
            return redirect('password')

    context = {
        'update':update
    }

    return render (request, 'password.html', context)

@login_required(login_url='loginpage')
def addtocart(request):
    if request.method == 'POST':
        basket_code = str(uuid.uuid4())
        vol = request.POST['itemquant']
        pid = request.POST['itemid']
        itemid = Product.objects.get(pk=pid)
        cart = ShopCart.objects.filter(user__username= request.user.username, paid_item=False)
        if cart: 
            basket = Shopcart.objects.get(products_id=itemid.id,user__username= request.user.username,)
            if basket:
                basket.quantity += vol
                basket.save()
                messages.success(request, 'product adddd to basket!')
                return redirect('products')
            else:
                newitem = ShopCart()
                newtiem.User = request
                newtiem.Product = itemid
                newtiem.quantity = vol
                newtiem.paid_item = False
                newtiem.cart_no = cart[0].cart_no
                newtiem.save()
                messages.successful(request, 'product added to Basket!')
                return redirect('products')
        else:
                newbasket = ShopCart()
                newbasket.user= request.user
                newbasket.product= itemid
                newbasket.quantity= vol
                newbasket.paid_item= False
                newbasket.cart_no = basket_code
                newbasket.save()
                messages.success(request, 'product added to basket')
                return redirect('products')


@login_required(login_url='loginpage')
def cart(request):
    basket = ShopCart.objects.filter(user__username = request.user.username, paid_item = False)

    subtotal = 0
    vat = 0
    total = 0

    for item in basket:
        subtotal += item.product.price * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'basket':basket,
        'subtotal':subtotal,
        'vat':vat,
        'total':total
    }


    return render(request, 'cart.html', context)


def deleteitem(request):
    remove = request.POST['delitem']
    ShopCart.objects.filter(pk=remove).delete()
    messages.success(request, 'item successfully deleted!')
    return redirect('cart')

def increase(request):
    add = request.POST['additems']
    addid = request.POST['itemid']
    adjust = ShopCart.objects.get(pk=addid)
    adjust.quantity = add
    adjust.save()
    message.success(request, 'item quantity Adjusted!')
    return redirected('cart')

def checkout(request):
    basket = ShopCart.objects.filter(user__username = request.user.username, paid_item = False)

    subtotal = 0
    vat = 0
    total = 0

    for item in basket:
        subtotal += item.product.price * item.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat

    context = {
        'basket':basket,
        'total':total,
        'cart_code': basket[0].cart_no
    }
    return render(request, 'checkout.html',context)

@login_required(login_url='loginpage')
def sendorder(request):
    if request.method == 'POST':
        api_key = 'sk_test_f0a5a8b92ea759bd42326fce0253c74bf3fc8ac9'
        curl = 'https://api.paystack.co/transaction/initialize'
        # cburl = 'http://127.0.0.1:8000/completed'
        # cburl = 'http://3.140.1.114/completed'
        cburl = 'http://3.133.92.138/completed'
        

        price = float(request.POST['price']) * 100
        bag_num = request.POST['bag']
        user = User.objects.get(username = request.user.username)
        pay_num = str(uuid.uuid4())
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        address = request.POST['adderess']
        state = request.POST['state']

        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':pay_num, 'email':user.email, 'amount':int(price), 'order_number':bag_num, 'callback_url':cburl}

        try:
            r = requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']

            paid = Payment()
            paid.user = user
            paid.paid_item = True
            paid.cart_no = bag_num
            paid.pay_code = pay_num
            paid.first_name = first_name
            paid.last_name = last_name
            paid.phone = phone
            paid.address = address
            paid.state = state
            paid.save()

            bag = ShopCart.objects.filter(user__username = request.user.username, paid_item=False)
            for item in bag:
                item.paid_item = True
                item.save()

                new_quantity = Product.objects.get(pk= item.product.id)
                new_quantity.max_quant -= item.quantity
                new_quantity.save()

            return redirect(rd_url)
        return redirect('checkout')

@login_required(login_url='loginpage')
def completed(request):
    user = User.objects.get(username= request.user.username)

    context = {
        'user':user
    }


    return render(request, 'completed.html',context)


    



