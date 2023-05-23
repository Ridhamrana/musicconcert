from django.shortcuts import render,redirect
from .models import User,Product,Cart,Transaction
from django.conf import settings
from django.core.mail import send_mail
import random
import razorpay
from django.http import JsonResponse

# Create your views here.
def form_validation(request):
	email=request.GET.get('email', None)
	data={'is_taken': User.objects.filter(email_iexact=email).exists()}

	return JsonResponse(data)

def index(request):
	try:
		products=Product.objects.all()
		user=User.objects.get(email=request.session['email'])
		carts=Cart.objects.filter(user=user,payment_status=False)
		request.session['cart_count']=len(carts)
		return render(request,"index.html",{'products':products})
	except:
		products=Product.objects.all()
		return render(request,"index.html",{'products':products})


def seller_index(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,"seller_index.html",{'products':products})

def about(request):
	return render(request,"about.html")

def blog(request):
	return render(request,"blog.html")

def seller_blog(request):
	return render(request,"seller_blog.html")

def events(request):
	products=Product.objects.all()
	return render(request,"events.html",{'products':products})


def contacts(request):
	return render(request,"contacts.html")

def seller_contacts(request):
	return render(request,"seller_contacts.html")



def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg1="Email Already Exist"
			return render(request,"signup.html",{'msg1':msg1})

		except:
			if request.POST['password'] == request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					mobile=request.POST['mobile'],
					email=request.POST['email'],
					password=request.POST['password'],
					usertype=request.POST['usertype'],
				)

				msg="Sign Up Successful"
				return render(request,"signup.html",{'msg':msg})

			else:
				msg1="Password and Confim Password Does Not Matched !!!"
				return render(request,"signup.html",{'msg1':msg1})

	else:
		return render(request,"signup.html")

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],password=request.POST['password'])
			if user.usertype=="Organizer":
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['lname']=user.lname
				return render(request,"seller_index.html")

			else:
				products=Product.objects.all()
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['lname']=user.lname
				carts=Cart.objects.filter(user=user,payment_status=False)
				request.session['cart_count']=len(carts)
				return render(request,"index.html",{'products':products})

		except Exception as e:
			print(e)
			msg1="Email or Password Does Not Matched!!!"
			return render(request,"login.html",{'msg1':msg1})

	else:
		return render(request,"login.html")

def logout(request):

	try:

		del request.session['email']
		del request.session['fname']
		del request.session['cart_count']
		return render(request,'login.html')
	
	except:

		return render(request,'login.html')
def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])

		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')

			else:
				msg1="New Password & Confirm New Passwrd Does Not Matched !!!"
				return render(request,'change_password.html',{'msg1':msg1})

		else:
				msg1="Old Passwrd Does Not Matched !!!"
				return render(request,'change_password.html',{'msg1':msg1})

	else:
		return render(request,'change_password.html')


def profile(request):
	user=User.objects.get(email=request.session['email'])
	return render(request,'profile.html',{'user':user})


def edit_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.save()
		msg="Profile Updated Successfully"
		return render(request,'login.html',{'user':user,'msg':msg})

	else:
		return render(request,'edit_profile.html',{'user':user})


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp = random.randint(1000,9999)
			subject = 'OTP - Forgot Password'
			message = "Hello "+user.fname+ ", Your OTP : "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail( subject, message, email_from, recipient_list )
			msg="OTP Sent Successful"
			return render(request,'verify_otp.html',{'email':user.email,'otp':otp,'msg':msg})

		except Exception as e:
			print(e)
			print("Hello1")
			msg1="Email Does Not Exist !!!"
			return render(request,'forgot_password.html',{'msg1':msg1}) 

	else:
		return render(request,'forgot_password.html')


def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'new_password.html',{'email':email})

	else:
		msg1="OTP Does Not Matched !!!"
		return render(request,'verify_otp.html',{'email':email, 'otp':otp,'msg1':msg1})


def new_password(request):
	
	if request.POST['new_password']==request.POST['cnew_password']:
		user = User.objects.get(email=request.POST['email'])
		user.password=request.POST['new_password']
		user.save()

		return redirect('login')

	else:
		msg1="New Password & Condirm New password Does Not 'Matched !!!"
		return render(request,'new_password.html',{'email':email, 'msg1':msg1})

def seller_profile(request):
	user=User.objects.get(email=request.session['email'])
	return render(request,'seller_profile.html',{'user':user})

def seller_edit_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.email=request.POST['email']
		user.save()
		msg="Profile Updated Successfully"
		return render(request,'login.html',{'user':user,'msg':msg})

	else:
		return render(request,'edit_profile.html',{'user':user})

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])

		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')

			else:
				msg1="New Password & Confirm New Passwrd Does Not Matched !!!"
				return render(request,'seller_change_password.html',{'msg1':msg1})

		else:
				msg1="Old Passwrd Does Not Matched !!!"
				return render(request,'seller_change_password.html',{'msg1':msg1})

	else:
		return render(request,'seller_change_password.html')


def seller_add_product(request):

	if request.method=="POST":
		seller=User.objects.get(email=request.session['email'])
		Product.objects.create(
				seller=seller,
				product_name=request.POST['product_name'],
				product_price=request.POST['product_price'],
				product_qty=request.POST['product_qty'],
				product_desc=request.POST['product_desc'],
				product_image=request.FILES['product_image'],
				product_venue=request.POST['venue'],
				product_time=request.POST['time'],
				product_date=request.POST['date'],
			)

		msg="Concert Added Successfully"
		return render(request,'seller_add_product.html',{'msg':msg})

	else:
		return render(request,'seller_add_product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller_view_product.html',{'products':products})

def seller_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller_product_detail.html',{'product':product})

def seller_product_edit(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_name=request.POST['product_name']
		product.product_desc=request.POST['product_desc']

		try:
			product.product_image=request.FILES['product_image']
			product.product_qty=request.POST['product_qty']
			product.product_price=request.POST['product_price']
			product.product_venue=request.POST['product_venue']
			product.product_date=request.POST['product_date']
			product.product_time=request.POST['product_time']

		except:
			pass
		
		product.save()
		msg="Concert Updated Successfully"
		return render(request,'seller_product_detail.html',{'product':product, 'msg':msg})

	else:
		return render(request,'seller_product_edit.html',{'product':product})

def seller_product_delete(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller_view_product')

def product_detail(request,pk):
	cart_flag=False
	product=Product.objects.get(pk=pk)
	
	try:
		user=User.objects.get(email=request.session['email'])
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass

	return render(request,'product_detail.html',{'product':product,'cart_flag':cart_flag})

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		net_price+=i.total_price
	request.session['cart_count']=len(carts)
	client = razorpay.Client(auth = (settings.KEY_ID,settings.KEY_SECRET))
	payments=client.order.create({'amount':net_price*100, 'currency':'INR', 	'payment_capture':1})
	carts.razorpay_order_id=payments['id']
	for i in carts:
		i.save()
	return render(request,'cart.html',{'carts':carts,'net_price':net_price,'payments':payments})

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(user=user,
		product=product,
		product_qty=1,
		product_price=product.product_price,
		total_price=product.product_price
		)

	return redirect('cart')

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.get(user=user,product=product).delete()
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return redirect('cart')

def change_qty(request):
	pk=request.POST['cid']
	product_qty=int(request.POST['product_qty'])
	cart=Cart.objects.get(pk=pk)
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')

def success(request):
	
	try:
		user=User.objects.get(email=request.session['email'])
		order_id=request.GET.get('order_id')
		carts=Cart.objects.filter(razorpay_order_id=order_id)
		for i in carts:
			i.payment_status=True
			i.save()
		msg="Payment Successful..."
		carts.delete()
		return render(request,'callback.html',{'msg':msg,'user':user,'carts':carts})
	except:
		order_id=request.GET.get('order_id')
		carts=Cart.objects.filter(razorpay_order_id=order_id)
		for i in carts:
			i.payment_status=True
			i.save()
		msg="Payment Successful..."
		carts.delete()
		return render(request,'callback.html',{'msg':msg,'carts':carts})

def Transaction(request):
	user=User.objects.get(email=request.session['email'])
	t=Transaction.objects.filter(user=user)
	return render(request,'Transaction_history.html',{'t':t})


