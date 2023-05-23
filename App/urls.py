from django.urls import path,include
from . import views
urlpatterns=[
       path('',views.index,name='index'),
       path('about/',views.about, name='about'),
       path('events/',views.events, name='events'), 
       path('blog/',views.blog, name='blog'),
	   path('seller_blog/',views.seller_blog, name='seller_blog'),
	   path('contacts/',views.contacts, name='contacts'),
       path('seller_contacts/',views.seller_contacts, name='seller_contacts'),
       path('login/',views.login, name='login'),
       path('signup/',views.signup, name='signup'),
       path('logout/',views.logout, name='logout'),
       path('profile/', views.profile, name='profile'),
       path('edit_profile/',views.edit_profile, name='edit_profile'),
       path('change_password/',views.change_password, name='change_password'),
       path('forgot_password/',views.forgot_password, name='forgot_password'),
       path('verify_otp/',views.verify_otp, name='verify_otp'),
       path('new_password/', views.new_password, name='new_password'),
       path('seller_profile/', views.seller_profile, name='seller_profile'),
       path('seller_edit_profile/',views.seller_edit_profile, name='seller_edit_profile'),
       path('seller_index/',views.seller_index,name='seller_index'),
       path('seller_change_password/',views.seller_change_password, name='seller_change_password'),
       path('seller_add_product/',views.seller_add_product,name='seller_add_product'),
       path('seller_view_product/',views.seller_view_product,name='seller_view_product'),
       path('seller_product_detail/<int:pk>/',views.seller_product_detail,name='seller_product_detail'),
       path('seller_product_edit/ <int:pk>/',views.seller_product_edit,name='seller_product_edit'),
       path('seller_product_delete/<int:pk>/',views.seller_product_delete,name='seller_product_delete'),
       path('product_detail/<int:pk>/',views.product_detail,name='product_detail'),
	   path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
	   path('cart/',views.cart,name='cart'),
	   path('remove_from_cart/<int:pk>',views.remove_from_cart,name='remove_from_cart'),
	   path('change_qty/',views.change_qty,name='change_qty'),
	   path('success/', views.success, name='success'),
	   path('ajax/form_validation//', views.form_validation, name='form_validation'),
	   path('Transaction/', views.Transaction, name='Transaction'),

   
    

]