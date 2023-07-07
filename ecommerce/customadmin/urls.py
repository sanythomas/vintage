from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.adminlogin, name = 'adminlogin'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('adminout/', views.adminout, name = 'adminout'),

    path('customer/', views.customer, name = 'customer'),
    path('customer/blockcustomer/<int:id>/', views.blockcustomer, name = 'blockcustomer'),
    path('customer/unblockcustomer/<int:id>/', views.unblockcustomer, name = 'unblockcustomer'),

   
    path('offer/', views.offer, name = 'adminoffer'),
    path('offer/addoffer/', views.addOffer, name = 'addoffer'),
    path('offer/editoffer/<int:oid>/', views.editOffer, name = 'editoffer'),
    path('offer/deleteoffer/<int:oid>/', views.deleteOffer, name = 'deleteoffer'),

    path('products/', views.products, name = 'products'),
    path('products/addproduct/',views.addproduct, name = 'addproduct'),
    path('products/product-attribute/<int:id>/',views.view_product_attribute, name = 'productattribute'),
    path('products/add-product-attribute/<int:id>/',views.add_product_attribute, name = 'addproductattribute'),
    path('products/edit-product-attribute/<int:id>/',views.edit_product_attribute, name = 'editproductattribute'),

    path('products/editproduct/<int:id>/',views.editproduct, name = 'editproduct'),
    path('products/deleteproduct/<int:id>/',views.deleteproduct, name = 'deleteproduct'),
    

    path('coupons/', views.coupons, name = 'admincoupons'),
    path('coupons/addcoupon/', views.addcoupon, name = 'addcoupon'),
    path('coupons/editcoupon/<int:cid>/', views.editcoupon, name = 'editcoupon'),
    path('coupons/deletecoupon/<int:cid>/', views.deletecoupon, name = 'deletecoupon'),


    path('category/', views.category, name = 'category'),
    path('category/addcategory', views.addcategory, name = 'addcategory'),
    path('category/editcategory/<int:id>/',views.editcategory, name = 'editcategory'),
    path('category/deletecategory/<int:id>/',views.deletecategory, name = 'deletecategory'),

    path('color/', views.color, name='color'),
    path('color/addcolor', views.addcolor, name = 'addcolor'),
    path('color/editcolor/<int:id>/',views.editcolor, name = 'editcolor'),
    path('color/deletecolor/<int:id>/',views.deletecolor, name = 'deletecolor'),

    path('size/', views.size, name = 'size'),
    path('size/addsize', views.addsize, name = 'addsize'),
    path('size/editsize/<int:id>/',views.editsize, name = 'editsize'),
    path('size/deletesize/<int:id>/',views.deletesize, name = 'deletesize'),

    path('order/', views.order, name = 'adminorder'),
    path('order/addorder', views.addorder, name = 'addorder'),
    path('order/addorderitem', views.addorderitem, name = 'addorderitem'),
    path('order/deleteorder/<int:id>/',views.deleteorder, name = 'deleteorder'),
    path('order/updateorder/<int:id>/',views.editorder, name = 'updateorder'),
    
]