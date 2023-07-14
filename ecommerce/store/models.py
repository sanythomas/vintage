
import decimal
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length = 13, unique=True, null=True, blank=True,)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=50,null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)


class Offer(models.Model):
    discount = models.IntegerField(default=0, null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

   

class Category(models.Model):
    category_name=models.CharField(max_length=50)
    image= models.ImageField(upload_to="images",default="")
    offer = models.ForeignKey(Offer,on_delete=models.SET_NULL, null=True, blank=True)
    


    def __str__(self):
        return self.category_name

class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100, default='Black')
    color_code = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return str(self.color_name)

class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return str(self.size_name)

class Products(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    image= models.ImageField( null=True, blank=True)
    image1= models.ImageField( null=True, blank=True)
    image2= models.ImageField( null=True, blank=True)
    image3= models.ImageField( null=True, blank=True)
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    offer = models.ForeignKey(Offer,on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ManyToManyField(ColorVariant, blank=True )
    size_variant = models.ManyToManyField(SizeVariant, blank=True )
    

   


    def __str__(self):
        return str(self.name)
        
    @property
    def offerPrice(self):
        offerPrice_decimal = self.price - (self.price * decimal.Decimal(self.offer.discount) * decimal.Decimal(0.01))
        offerPrice = int(offerPrice_decimal)
        return offerPrice
            
    def get_product_price_by_size(self, size):
        if self.offer:
            return self.offerPrice + SizeVariant.objects.get(size_name=size).price
        else:
            return self.price + SizeVariant.objects.get(size_name=size).price

    
           
    
    
    @property
    def imageURL(self):
        try:
            url =self.image.url
        except:
            url=''
        return url

    @property
    def image1URL(self):
        try:
            url =self.image1.url
        except:
            url=''
        return url

    @property
    def image2URL(self):
        try:
            url =self.image2.url
        except:
            url=''
        return url

    @property
    def image3URL(self):
        try:
            url =self.image3.url
        except:
            url=''
        return url




class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length = 13, null=True, blank=True,)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


 
class Order(models.Model):
    STATUS = (
			('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Shipped', 'Shipped'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
			)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shippingaddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    

    def __str__(self):
        return str(self.id)


    @property
    def get_cart_total(self):
        try:
            orderitems = self.orderitem_set.all()
            total = sum([item.get_total for item in orderitems])
        
            return total
        except:
            pass
       

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        try:
            total = sum([item.quantity for item in orderitems])
        
            return total

        except:
            pass




class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def updated_price_by_size(self):
        if self.product.offer:
            return self.product.offerPrice + SizeVariant.objects.get(size_name=self.size_variant).price
        else:
            return self.product.price + SizeVariant.objects.get(size_name=self.size_variant).price

    @property
    def get_total(self):

        if self.product.offer and self.size_variant:
            price = [self.product.offerPrice]
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
            variant_price = sum(price)
            total = variant_price * self.quantity
            return total

        if self.product.offer:
            total = self.product.offerPrice * self.quantity
            return total
                
        if  self.size_variant:
            price = [self.product.price]
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
            variant_price = sum(price) 
            total = variant_price * self.quantity
            return total
        else:
            total = self.product.price * self.quantity
            return total

  
    

class Coupons(models.Model):
    couponcode = models.CharField(max_length=200, null=True)
    percent = models.IntegerField(default = 0, null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)






