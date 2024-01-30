from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Reg,Log
from thursdayapp.models import product
from django.db.models import Q
import random
from .models import product,Cart,Order
import razorpay
from django.core.mail import send_mail


def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        ucpass=request.POST["ucpass"]
        if uname=="" or upass=="" or ucpass=="":
            context["errmsg"]="Fields cannot be empty"
            return render(request,"registration.html",context)
        elif upass!=ucpass:
            context["errmsg"]="password and confirm password didn't match"
            return render(request,"registration.html",context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context["success"]="User created successfully"
                return render(request,"registration.html",context)

            except Exception:
                context["success"]="user with same username already exists"
                return render(request,"registration.html",context)
    else:
        return render(request,"registration.html",context)        
    
    

def user_login(request):
    context = {}

    if request.method == "POST":
        uname = request.POST.get("uname")
        upass = request.POST.get("upass")

        if not uname or not upass:
            context["errmsg"] = "Fields cannot be empty"
            return render(request, "loginpage.html", context)

        user = authenticate(request, username=uname, password=upass)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            context["errmsg"] = "Invalid username or password"
            return render(request, "loginpage.html", context)
    else:
        return render(request, "loginpage.html", context)
    

def user_logout(request):
    # Logout the user and redirect to the homepage
    logout(request)
    return redirect("home")  # You can use a URL name defined in your URLs

def catfilter(request, cv):
    # Filter products by category
    q = Q(is_active=True, cat=cv)  # Combine conditions using a single Q object
    products = product.objects.filter(q)
    
    context = {'products': products}
    return render(request, 'index.html', context)

def home(request):
    # Display all active products
    products = product.objects.filter(is_active=True)
    context = {'products': products}
    return render(request, "index.html", context)

def sort(request, sv):
    print(type(sv))
    if sv == "0":
        col="-pcost"
    else:
        col="pcost"
    
    p = product.objects.filter(is_active=True).order_by(col)
    context = {}
    context["products"]=p
    return render(request,"index.html",context)

def range(request):
    min_value = request.GET.get('min', None)
    max_value = request.GET.get('max', None)

    if min_value is not None and max_value is not None:
        try:
            min_value = float(min_value)
            max_value = float(max_value)

            q1 = Q(pcost__gte=min_value)
            q2 = Q(pcost__lte=max_value)
            q3 = Q(is_active=True)
            products = product.objects.filter(q1 & q2 & q3)
        except ValueError:
            # Handle invalid input values (non-numeric or empty strings)
            products = []
    else:
        # Handle case when 'min' and 'max' parameters are missing or empty
        products = []

    context = {'products': products}
    return render(request, 'index.html', context)



def cart(request):
    return render(request,"cart.html")


def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,"contact.html")

def details(request):
    return render(request,'details.html')

def product_details(request,pid):
    context={}
    context["products"]=product.objects.filter(id=pid)
    return render(request,"products.html",context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        p=product.objects.filter(id=pid)
        print(p)
        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        return HttpResponse("product added in the cart")
    else:
        return redirect("/login")


# from django.shortcuts import get_object_or_404

# def remove(request, cid):
#     cart_item = get_object_or_404(Cart, id=cid)
#     cart_item.delete()
#     return redirect("/viewcart")

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")

def removes(request, cid):
    print(f"Removing item with ID: {cid}")
    c = Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/placeorder")


def viewcart(request):
    user_id=request.user.id
    c=Cart.objects.filter(uid=user_id)
    s=0
    np=len(c)
    for x in c:
        s=s+x.pid.pcost*x.qty
    context={}
    context['n']=np
    context['products']=c
    context['total']=s
    return render(request,"cart.html",context)


def updateqty(request,qv,cid):
    print(type(qv))
    c=Cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    # print(c[0].qty)
    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(c)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.pcost*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['n']=np
    return render(request,'placeorder.html',context)




   
def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.pcost*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_panmLCg4SS41cu", "v30k2xGiMqArElf3rGmIpNSt"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['data']=payment
    context['amt']=payment['amount']*100
    return render(request,"pay.html",context)

# def remove(request,cid):
#     c=Cart.objects.filter(id=cid)
#     c.delete()
#     return redirect("/")

def sendusermail(request):
        uemail=request.user.email
        print(uemail)
        msg="order details are:"
        send_mail(
        "Ekart order placed successfully!",
        msg,
        "manjulamukkamalla13@gmail.com",
        [uemail],
        fail_silently=False,
        )
        return HttpResponse("mail send successfully")
from django.core.mail import send_mail