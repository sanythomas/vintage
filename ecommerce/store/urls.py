from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('shop/', views.store, name = 'shop'),
    path('category/<str:categoryname>/', views.categoryView, name = 'categoryview'),
    path('shop/shop-details/<int:id>/', views.shop_details, name = 'shop-details'),
    path('shop/shop-details/<int:id>/size-change/', views.size_change, name = 'size-change'),

    path('shop/search/', views.search, name = 'search'),
    path('shop/cart/', views.cart, name = 'cart'),

    path('blog/', views.blog, name = 'blog'),
    path('contact/', views.contact, name = 'contact'),
    path('about/', views.about, name = 'about'),
    path('signout/', views.signout, name = 'signout'),
    path('signin/', views.signin, name = 'signin'),
    path('signup/', views.signup, name = 'signup'),
    path('otplogin/', views.otplogin, name = 'otplogin'),
    path('otp/', views.otp, name = 'otp'),
    path('shop/checkout/', views.checkout, name = 'checkout'),
    path('update_item/', views.updateItem, name = 'update_item'),
    path('add_address/', views.addshippingAddress, name = 'add_address'),
    path('process_order/', views.processOrder, name = 'process_order'),
    path('add_coupon/', views.addCoupon, name='add_coupon'),
    path('account/', views.profile, name = 'account'),
    path('orders/', views.myOrders, name = 'orders'),
    path('cancel_order/', views.cancelOrder, name = 'cancel-order'),
    path('my-addressbook/',views.my_addressbook, name='my-addressbook'),
    path('add-address/',views.save_address, name='add-address'),
    path('activate-address/',views.activate_address, name='activate-address'),
    path('update-address/<int:id>/',views.update_address, name='update-address'),

    path('wishlist/', views.wishlist, name = 'wishlist'),
    path('add_to_wishlist/', views.addToWishlist, name = 'add_to_wishlist'), 
    path('delete_from_wishlist/', views.deleteFromWishlist, name = 'delete_from_wishlist'), 
   
    path('view_invoice/<int:order_id>', views.view_invoice, name = 'view_invoice'),
    
    path('coupons/', views.coupons, name = 'coupons'),

    path('order-complete/', views.order_complete, name = 'order_complete')


    
]
