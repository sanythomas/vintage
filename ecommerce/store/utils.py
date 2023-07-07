import json
from . models import *
from django.contrib import messages


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
    else:
        try:
            device = request.COOKIES['device']
        except:
            device = {}
      
            # device = ''
        customer, created = User.objects.get_or_create(device=device, username = device)
        print(customer.device)

    order, created = Order.objects.get_or_create(user=customer, complete=False, status='Pending')

    items = order.orderitem_set.all()
   
    cartItems = order.get_cart_items
    
    

  

    return {'cartItems':cartItems, 'order':order, 'items':items,}

