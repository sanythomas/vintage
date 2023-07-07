
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from store.models import *
from django.db.models import Q

# Create your views here.

@never_cache
def adminlogin(request):
    if 'useradmin' in request.session:
        return redirect(dashboard)
    if request.method == 'POST':
        useradmin = request.POST['useradmin']
        password = request.POST['password']
        user = auth.authenticate(username=useradmin, password = password)
        if user is not None and user.is_superuser:
            auth.login(request,user)
            print(user.is_anonymous)
            request.session['useradmin'] = useradmin
            return redirect (dashboard)
        else:
            messages.error(request, 'Invalid Credintials!!!')
            return redirect(adminlogin)
    return render(request,'customadmin/page-login.html')


@never_cache
def dashboard(request):
    if 'useradmin' in request.session:
        orders = Order.objects.filter(complete = True)
        products = Products.objects.all()
        orders_delivered = Order.objects.filter(status = 'Delivered')
   
        context = {'orders':orders, 'products':products, 'orders_delivered':orders_delivered}
        return render(request, 'customadmin/dashboard.html', context)
    return redirect (adminlogin)

@never_cache
def adminout(request):
    if 'useradmin' in request.session:
        request.session.flush()
    return redirect (adminlogin)

def customer(request):
    if 'useradmin' in request.session:
        UserList = User.objects.filter(~Q(first_name='')).order_by('-id')
        # UserList = User.objects.all()
        context = {'user': UserList}
        return render(request, 'customadmin/customer.html', context)

def blockcustomer(request,id):
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('customer')

def unblockcustomer(request,id):
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('customer')


def category(request):
    CategoryList = Category.objects.all().order_by('-id')
    context = {'category': CategoryList}
    return render (request, 'customadmin/category.html', context)



def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category = Category.objects.create(category_name=category_name)
        category.save()
        print('category added')
        return redirect ('category')
    else:
        offer = Offer.objects.all()
        context = {'offer':offer}
        return render (request, 'customadmin/add_category.html', context)

def deletecategory(request,id):
    category = Category.objects.filter(id=id)
    category.delete()
    return redirect('category')

def editcategory(request,id):
    if request.method == 'POST':
        category_name = request.POST['category']
        offerid = request.POST['offerid']
        currentcategory = Category.objects.get(id=id)
        currentcategory.category_name = category_name
        currentcategory.offer_id = offerid
        for product in currentcategory.products_set.all():
            product.offer_id = offerid
            product.save()
        currentcategory.save()
        return redirect ('category')

    category = Category.objects.all()
    offer = Offer.objects.all()
    currentcategory = Category.objects.get(id=id)
    context = { 'category':category, 'offer':offer, 'currentcategory':currentcategory}
    return render(request, 'customadmin/edit_category.html', context)

def color(request):
    ColorList = ColorVariant.objects.all()
    context = {'color': ColorList}
    return render (request, 'customadmin/color.html', context)


def addcolor(request):
    if request.method == 'POST':
        color_name = request.POST['color_name']
        color_code=request.POST['color_code']
        price= request.POST['price']
        ColorVariant.objects.create(color_name=color_name, color_code=color_code, price=price)
        print('color added')
        return redirect ('color')
    
    context = {}
    return render(request, 'customadmin/add_color.html', context)

def editcolor(request, oid):
    color = ColorVariant.objects.get(id=id)
    context = {'color':color}
    return render(request, 'customadmin/edit_color.html', context)

def deletecolor(request, oid):
    color = ColorVariant.objects.get(id=id)
    color.delete()
    return render(request, 'customadmin/color.html')


def size(request):
    SizeList = SizeVariant.objects.all()
    context = {'size': SizeList}
    return render (request, 'customadmin/size.html', context)


def addsize(request):
    if request.method == 'POST':
        size_name = request.POST['size_name']
        price= request.POST['price']
        SizeVariant.objects.create(size_name=size_name, price=price)
        print('size added')
        return redirect ('size')
    
    context = {}
    return render(request, 'customadmin/add_size.html', context)

def editsize(request, id):
    size = SizeVariant.objects.get(id=id)
    context = {'size':size}
    return render(request, 'customadmin/edit_size.html', context)

def deletesize (request, id):
    size = SizeVariant.objects.get(id=id)
    size.delete()
    return render(request, 'customadmin/size.html')


def products(request):
    products = Products.objects.order_by('-id')
   
    context = {'products': products,}
    return render(request, 'customadmin/products.html', context)

def addproduct(request):
    if request.method=='GET':
        offer = Offer.objects.all()
        category=Category.objects.all()
        color=ColorVariant.objects.all()
        size=SizeVariant.objects.all()
        return render(request,'customadmin/add_products.html',{'category':category, 'offer':offer, 'color':color, 'size':size})

    if request.method == 'POST':
        product_name = request.POST['product_name']
        price = request.POST['price']
        stock = request.POST['stock']
        color=request.POST['color']
        size=request.POST['size']
        description = request.POST['description']
        image = request.FILES['image']
     
        Products.objects.create(name=product_name, price=price, stock=stock, description=description,category_id=category, color=color, size=size, image=image)
                
   
        print('product added')
        return redirect(products)

def view_product_attribute(request, id):

    product = Products.objects.get(id=id)
    context = {'product':product}
    return render(request, 'customadmin/product_attribute.html', context)

def add_product_attribute(request, id):
    
    context = {}
    return render(request, 'customadmin/add_product_attribute.html', context)


def edit_product_attribute(request,id):
    pass


def editproduct(request,id):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        price = request.POST['price']
        stock = request.POST['stock']
        description = request.POST['description']
        category = request.POST['category']
        offer = request.POST['offerid']


        product = Products.objects.get(id=id)
        product.name = product_name
        product.price = price
        product.stock = stock
        product.description = description
        product.category_id=category
        product.offer_id=offer
        product.image = request.FILES.get('image',product.image)
        product.image1 = request.FILES.get('image1',product.image1)
        product.image2 = request.FILES.get('image2',product.image2)
        product.image3 = request.FILES.get('image3',product.image3)
       
        
        
        product.save()
        
        return redirect (products)
    else:
        product=Products.objects.get(id=id)
        print(type(product.image1))
        category = Category.objects.all()
        offer = Offer.objects.all()
        return render(request, 'customadmin/edit_product.html',{'product': product, 'category':category, 'offer':offer})

def deleteproduct(request, id):
    product = Products.objects.filter(id=id)
    product.delete()
    return redirect('products')



def order(request):
    orders = Order.objects.filter(~Q(status='Pending')).order_by('-id')
    context = {'orders':orders}
    return render(request, 'customadmin/order.html', context)

def addorder(request):
    if request.method=='GET':
        user = User.objects.all()
        product = Products.objects.all()
      
        context = {'user':user, 'product': product}
        return render(request,'customadmin/add_order.html',context)

    if request.method == 'POST':
        user_id = request.POST['user']
        complete = request.POST['complete']
        transaction_id = request.POST["transaction_id"]
        

        Order.objects.create(user_id=user_id, complete=complete, transaction_id=transaction_id)
        
        print('Order added')
        return redirect('order')

def addorderitem(request):
    if request.method=='GET':
        product = Products.objects.all()
        order = Order.objects.all()
      
        context = {'order':order, 'product': product}
        return render(request,'customadmin/add_orderitem.html',context)

    if request.method == 'POST':
        product_id = request.POST['product']
        order_id = request.POST['order_id']
        quantity = request.POST["quantity"]
     

        OrderItem.objects.create(product_id=product_id, order_id=order_id, quantity=quantity)
        
        print('Orderitem added')
        return redirect('order')

def editorder(request,id):
    if request.method == 'POST':
        user_id = request.POST['first_name']
        shipping_id = request.POST['shippingaddress']
        complete = request.POST['complete']
        print(complete)
        transaction_id = request.POST['transaction_id']
        status = request.POST['status']
        order = Order.objects.get(id=id) 
        order.user_id = user_id
        order.shippingaddress_id = shipping_id
        order.complete = complete
        order.transaction_id = transaction_id
        order.status = status
        order.save()
        return redirect ('adminorder')
        
    order = Order.objects.get(id=id) 
    user = User.objects.all()
    shippingaddress = ShippingAddress.objects.all()
    print(order.status)
    for i in order.STATUS:
        print(i[1])
    context = {'order':order, 'user':user, 'shippingaddress':shippingaddress}
    return render(request, 'customadmin/edit_order.html', context)

def deleteorder(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('order')

    


def offer(request):
    offers = Offer.objects.all()

    context = {'offers':offers}
    return render(request, 'customadmin/offer.html', context)

def addOffer(request):
    if request.method == 'POST':
        discount = request.POST['discount']
        valid_from = request.POST['valid_from']
        valid_to = request.POST['valid_to']
        is_active = request.POST["is_active"]
        
        Offer.objects.create(discount=discount, valid_from=valid_from, valid_to=valid_to, is_active=is_active )
        return redirect(offer)

    
    context = {}
    return render(request, 'customadmin/add_offer.html', context)

def editOffer(request, oid):
    offer = Offer.objects.get(id=oid)
    context = {'offer':offer}
    return render(request, 'customadmin/edit_offer.html', context)

def deleteOffer(request, oid):
    offer = Offer.objects.get(id=oid)
    offer.delete()
    return render(request, 'customadmin/offer.html')




def coupons(request):
    coupons = Coupons.objects.all()
    context = {'coupons':coupons}
    return render(request, 'customadmin/coupons.html', context)

def addcoupon(request):
    if request.method == 'POST':
        couponcode = request.POST['couponcode']
        percent = request.POST['percent']
        valid_from = request.POST['valid_from']
        valid_to = request.POST['valid_to']
        Coupons.objects.create( couponcode=couponcode, percent=percent, valid_from=valid_from, valid_to=valid_to)
        return redirect(coupons)
    
    context = {}
    return render(request,  'customadmin/add_coupon.html', context)

def editcoupon(request, cid):
    if request.method == 'POST':
        couponcode = request.POST['couponcode']
        percent = request.POST['percent']

        coupon = Coupons.objects.get(id=cid)
        coupon.couponcode = couponcode
        coupon.percent = percent
        coupon.save()
        return redirect(coupons)
    
    coupon = Coupons.objects.get(id=cid)
    context = {'coupon':coupon}
    return render(request,  'customadmin/edit_coupon.html', context)

def deletecoupon(request, cid):

    coupon = Coupons.objects.get(id=cid)
    coupon.delete()
    return redirect(coupons)

    