

from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from store.mixins import MessageHandler
from django.http import JsonResponse
import json
import datetime
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
from .forms import *
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.


def signup (request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        phone1 = request.POST['phone']
        phone = '+91'+ phone1
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if password1==password2:
            if User.objects.filter(username=email).exists():
                messages.info(request,'User already exists')
                return redirect(signup)
            else:
                user = User.objects.create_user(first_name = fname, last_name = lname, phone_number=phone, username=email,  password=password1)
                user.save()
                print('user created')
                return redirect('signin')
                
        else:
            messages.info(request,'Passwords do not match')
            return redirect ('signup')

    return render(request,'store/signup.html')


def signin (request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = auth.authenticate(username=username, password = password)
        print(user)
        
        if user is not None:
            auth.login(request, user)
            # print(request.user.is_anonymous)
            request.session['username'] = username
           
            device = request.COOKIES['device']

            guest_customer = User.objects.get(device=device)
           

            user_open_order, created = Order.objects.get_or_create(complete=False, status='Pending', user_id = request.user.id)
            print(user_open_order)
          
            guest_open_order = Order.objects.get(complete=False, status='Pending', user_id = guest_customer.id)
            print(guest_open_order)


            guest_orderItems = OrderItem.objects.filter(order_id = guest_open_order.id)
            print(guest_orderItems)

            user_orderItems = OrderItem.objects.filter(order_id = user_open_order.id)
            print(user_orderItems)

            if user_orderItems.exists():

                for g_orderitem in guest_orderItems:
                    print(g_orderitem.product.name)
                    print(g_orderitem.quantity)

                    for u_orderitem in user_orderItems:
                        if user_orderItems.filter(product=g_orderitem.product):
                        # if guestuser's orderitem's product is present in current user's orderitems
                        # then check if the user orderitem (inner loop) is equal to the guest useritem (outerloop)
                            if u_orderitem.product == g_orderitem.product: 
                                if u_orderitem.size_variant == g_orderitem.size_variant:
                                    u_orderitem.quantity = u_orderitem.quantity + g_orderitem.quantity
                                    u_orderitem.save()
                                else:
                                    product = g_orderitem.product
                                    size_variant = g_orderitem.size_variant
                                    new_orderitem = OrderItem.objects.create(order = user_open_order, product = product, size_variant = size_variant)
            
                                    new_orderitem.quantity = new_orderitem.quantity + g_orderitem.quantity
                                    new_orderitem.save()
                            
                            
                        else:
                            # create a new order item with product from the guest user. 
                            product = g_orderitem.product
                            size_variant = g_orderitem.size_variant
                            new_orderitem = OrderItem.objects.create(order = user_open_order, product = product, size_variant = size_variant)
            
                            new_orderitem.quantity = new_orderitem.quantity + g_orderitem.quantity
                            new_orderitem.save()
            else:

                for g_orderitem in guest_orderItems:
                    product = g_orderitem.product
                    size_variant = g_orderitem.size_variant
                    new_orderitem = OrderItem.objects.create(order = user_open_order, product = product, size_variant=size_variant)
                    new_orderitem.quantity = g_orderitem.quantity
                    new_orderitem.save()

            guest_customer.delete()
            guest_open_order.delete()

            
            messages.error(request, 'Logged in Successfully')

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(home)
        else:
            messages.error(request, 'Invalid Credintials!!!')
            return redirect(signin)

    data = cartData(request)
    cartItems = data['cartItems']
    print(cartItems)
    order = data['order']
    try:
     wishlistcount = Wishlist.objects.filter(user=user).count()
    except:
        wishlistcount = '0'
    context = {'cartItems':cartItems,'order':order, 'wishlistcount':wishlistcount}
        
    return render(request,'store/signin.html', context)


def otplogin(request):
    if request.method=='POST':
        global phone
        phone1=request.POST['phone_number']
        phone = '+91'+ phone1
        print(phone)
        message_handler = MessageHandler(phone).sent_otp_on_phone()
        return redirect('otp')
    return render(request, 'store/otplogin.html')

def otp(request):
    if request.method=='POST':
        otp1= request.POST['otp']
        validate = MessageHandler(phone).validate(otp1)
        print("validate=",validate)
        if validate=="approved":
            user = User.objects.get(phone_number=phone)

            print(user.username)
            if user==None:
                messages.error(request, 'Wrong Credentials')
                return redirect('otp')
            auth.login(request,user)
           
            return redirect('home')

    return render(request, 'store/otp.html')




def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    print(cartItems)
    order = data['order']

    new_4_products = Products.objects.all().order_by('-id')[:4]
    product_with_offer = Products.objects.filter(~Q(offer_id = None))
    best_selling_product = OrderItem.objects.all().distinct("product_id")[:4]
   
    

    products = Products.objects.all()

    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()
    context = {'products':products, 'cartItems':cartItems,'order':order, 'wishlistcount':wishlistcount, 'new_4_products':new_4_products, 'product_with_offer':product_with_offer, 'best_selling_product':best_selling_product}
    return render(request, 'store/home.html', context)


def categoryView (request, categoryname):

    if (Category.objects.filter(category_name=categoryname)):
        products = Products.objects.filter(category__category_name=categoryname).order_by('-id')
        product_qty = Products.objects.filter(category__category_name=categoryname).count()
        for product in products:
            if product.offer:
                print(product.offerPrice)

            
                
                
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()
    categories = Category.objects.all()
    context= {'products':products, 'categories':categories,'cartItems':cartItems, 'order':order, 'wishlistcount':wishlistcount }
    return render(request, 'store/pages/category_view.html', context)


def profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'store/pages/profile.html',{'form':form,'msg':msg})



# def wishlist(request):
#     return render(request, 'store/pages/wishlist.html')

def coupons(request):
    coupons = Coupons.objects.all()
    return render(request, 'store/pages/coupons.html', {'coupons': coupons})

    
def store(request):

    ordering = request.GET.get('ordering', "")
    price = request.GET.get('price', "")

    
    products = Products.objects.all().order_by('-id')

    if ordering:
        products = products.order_by(ordering)
    if price:
        print(int(price)-100)
        products = products.filter(price__gte = price, price__lt = int(price)+100)

    #pagination 
    page_num = request.GET.get('page', 1)
    paginator = Paginator(products, 12)
    products = paginator.page(page_num)


    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    offer = Offer.objects.all()
    categories = Category.objects.all()

    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()
    size_variant = SizeVariant.objects.all()
    color_variant = ColorVariant.objects.all().order_by('id')
   
    
    context = {
        'products':products, 
        'cartItems':cartItems,
        'order':order, 
        'categories':categories, 
        'wishlistcount':wishlistcount, 
        'size_variant':size_variant,
        'color_variant':color_variant,
        
        }
    return render(request, 'store/store.html', context)


def search_results(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': # instead of request.is_ajax which is depreciated
        res = None
        search_products = request.POST.get('search_products')
        qs = Products.objects.filter(name__icontains=search_products)
        if len(qs) > 0 and len(search_products) > 0:
            data = []
            for pos in qs:
                item = {
                    'pk': pos.pk, 
                    'name': pos.name,
                    'image':str(pos.imageURL)
                    #'category':pos.category -> Got an error object of type Category is not JSON serializable
                }
                data.append(item)
                res = data
        else:
            res = 'No products found!'

        return JsonResponse({'data': res})

    return JsonResponse({})


def shop_details(request,id):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    product = Products.objects.get(id=id)


    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()
    context = {
        'product':product,
        'cartItems':cartItems,
        'order':order,
        'wishlistcount':wishlistcount
        }
    return render (request, 'store/pages/shop-details.html', context)

def size_change(request,id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = Products.objects.get(id=id)
        print(product)
        size = request.POST.get('size')
        price = product.get_product_price_by_size(size)
        print(price)

        response = {'updated_price':price}
        return JsonResponse (response)

    return JsonResponse({})
    


def blog(request):
    return render(request, 'store/blog.html')

def contact(request):
    return render(request, 'store/contact.html')

def about(request):
    return render(request, 'store/pages/about.html')
    
def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request,'Logged out successfully')
        return redirect('home')
        

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    
    
    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()

    context = {'items':items, 'order':order, 'cartItems':cartItems,'wishlistcount':wishlistcount}
    return render(request, 'store/pages/shopping-cart.html', context)
    
@login_required(login_url='signin')
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # coupon = data['coupon']
    # coupon_code_message = data['coupon_code_message']

    customer = request.user
    
    shippingaddress = customer.shippingaddress_set.all()
    print(shippingaddress)
    
    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shippingaddress':shippingaddress,'wishlistcount':wishlistcount, }
    return render(request, 'store/pages/checkout.html', context)


def updateItem(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')
        action = request.POST.get('action')
        size_variant = request.POST.get('size_variant')
        size_id = request.POST.get('size_id')
        print('sany')
        print(size_id)
        print(size_variant)
        print('Action:',action)
        print('productId:',productId)

        if request.user.is_authenticated:
            customer = request.user
        else:
            device = request.COOKIES['device']
            print(device)
            customer, created = User.objects.get_or_create(device=device)
            print(customer.device)

        
        product = Products.objects.get(id=productId)
        print(product)
        order, created = Order.objects.get_or_create(user=customer,complete = False, status='Pending')
        size_variant = SizeVariant.objects.get(size_name = size_variant)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, size_variant=size_variant)

        

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
            messages = 'Item added to cart'
        
        elif action == 'remove':
            if orderItem.quantity !=1:
                orderItem.quantity = (orderItem.quantity - 1)
                messages = 'Item removed from cart'
  
        orderItem.save()

        if action == 'delete':
            orderItem.delete()
            print('sany')
            messages = 'Product removed from cart'

        

        
        print(orderItem.product.name)
        print(order.get_cart_total)
        
        

        response = {'cartItems':order.get_cart_items, 'cartTotal':order.get_cart_total, 'itemTotal': orderItem.get_total, 'itemQty': orderItem.quantity, 'messages':messages}

        return JsonResponse(response, safe=False )

def addshippingAddress(request):
    if request.method == 'POST':
        customer = request.user
        ShippingAddress.objects.create(
            user = customer,
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            city = request.POST.get('city'),
            state = request.POST.get('state'),
            zipcode = request.POST.get('zipcode'),
        )
        
        shippingaddress = ShippingAddress.objects.last()
        # shippingaddress = ShippingAddress.objects.filter(user=customer)

        response = serializers.serialize("json", [shippingaddress]),
        print(response)
       
        # response = {'shippingaddress':shippingaddress}

    return HttpResponse(response, content_type="application/json")
    # return JsonResponse(response, safe=False )

def addCoupon(request):
    if request.method == 'POST':
        customer = request.user
        orderid = request.POST.get('orderid')
        order = customer.order_set.get(id=orderid)

        cart_total = request.POST.get('total')
        cart_total = int(float(cart_total))
        print(cart_total)
        print(type(cart_total))
        coupon = request.POST.get('couponcode')

        try:
            coupon = Coupons.objects.get(couponcode=coupon)
            coupon_discount = coupon.percent
            print(type(coupon_discount))
            print(coupon_discount)
        
            discounted_price = int(cart_total - (cart_total * .01 * coupon_discount))
            discounted_amount = int(cart_total * .01 * coupon_discount)
        
                

            response = {'discounted_price':discounted_price, 'coupon_discount':coupon_discount, 'discounted_amount':discounted_amount}

        except:
            coupon_code_message = 'Invalid Coupon Code!'
            print('Invalid coupon')
            response = {'error_message':coupon_code_message,}
        

    return JsonResponse(response, safe=False )



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer,complete = False)

    else:
        customer,order = guestOrder(request, data)

    total = float(data['orderdata']['total'])
    order.transaction_id = transaction_id
   

    if total == float(order.get_cart_total):
        print(total == float(order.get_cart_total))
        order.complete = True
        order.status = 'Confirmed'

    for orderItem in order.orderitem_set.all():
        print(orderItem.product.stock)
        orderItem.product.stock =   orderItem.product.stock - 1
        print( orderItem.product.stock)

    shippingaddressId = int(data ['orderdata']['shippingaddressId'])
    print(shippingaddressId)
    order.shippingaddress = ShippingAddress.objects.get(id=shippingaddressId)

    order.date_ordered = datetime.datetime.now()
    
    order.save()

    print(order)


   

    return JsonResponse('Payment complete', safe=False )


@login_required(login_url='signin')
def wishlist(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    wishlist = Wishlist.objects.filter(user=request.user)
    user=request.user.id
    wishlistcount = Wishlist.objects.filter(user=user).count()
    print(wishlistcount)

    context = {'wishlist':wishlist, 'wishlistcount':wishlistcount, 'cartItems':cartItems, 'order':order}
    return render (request, 'store/pages/wishlist.html', context)

def addToWishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('productId'))
            product_check = Products.objects.get(id=product_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=product_id)):
                    return JsonResponse({'status': "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user = request.user, product_id=product_id)
                    wishlistcount = Wishlist.objects.all().count()
                    return JsonResponse({'status': "Product added to wishlist", 'wishlistcount': wishlistcount})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')

def deleteFromWishlist(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('productId'))
        delete_wishlist = Wishlist.objects.filter(user=request.user, product_id=product_id)
        delete_wishlist.delete()
        wishlistcount = Wishlist.objects.all().count()
        return JsonResponse({'status': "item  removed from wishlist", "wishlistcount":wishlistcount})


def myOrders(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    customer = request.user
    orders = customer.order_set.all().order_by('-id')
   
    
    context = {'orders': orders, 'cartItems':cartItems,'order':order,}
    return render(request, 'store/pages/my_orders.html', context)

def cancelOrder(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId')
        order_to_cancel = Order.objects.get(id=orderId)
        order_to_cancel.status = 'Cancelled'
        order_to_cancel.save()

    return JsonResponse({'status': "Order cancelled",'order-status': order_to_cancel.status})

# My AddressBook
def my_addressbook(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	return render(request, 'store/pages/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'store/pages/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'store/pages/update-address.html',{'form':form,'msg':msg})
        

        
def view_invoice(request, order_id):
    
    current_order=Order.objects.get(id=order_id)
    print(current_order)
    
    orderitems = OrderItem.objects.filter(order_id = current_order.id)

    user = request.user
    
    template_path = 'store/pages/invoice.html'
   
   

    context = {'current_order': current_order, 'orderitems':orderitems, 'user': user}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="invoice.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def order_complete(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    wishlistcount = Wishlist.objects.all().count()
    context = {'cartItems':cartItems,'order':order, 'wishlistcount':wishlistcount }
    return render (request, 'store/pages/order_complete.html', context)