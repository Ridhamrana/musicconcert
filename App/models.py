from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	mobile=models.BigIntegerField()
	email=models.EmailField()
	password=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100,default="User")

	def __str__(self):
		return self.fname+" "+self.lname 

class Product(models.Model):
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=100)
	product_price=models.BigIntegerField()
	product_qty=models.IntegerField()
	product_desc=models.TextField()
	product_image=models.ImageField(upload_to="images/")
	product_venue=models.TextField(default="")
	product_time=models.TimeField(blank=True,null=True)
	product_date=models.DateField(blank=True,null=True)

	def __str__(self):
		return self.product_name+" - "+self.seller.fname

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	product_qty=models.IntegerField(default=1)
	product_price=models.IntegerField()
	payment_status=models.BooleanField(default=False)
	total_price=models.IntegerField(default=0)
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_name

class Transaction(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.fname+" "+self.user.lname

