from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
import razorpay

from .models import Artwork,Cart,Address,Payment,Order
from django.contrib import messages
from django.db.models import Q


from django.conf import settings
# Create your views here.
# //artist 123
def home(request):
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
        context={
            'ca':ca
        }
    return render(request, 'index.html',context)

def  about(request):
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
        context={
            'ca':ca
        }
    return render(request, 'about.html',context)

def register(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2= request.POST.get('confirmPassword')
        email = request.POST.get('email')
        print(username, password, email)
        my_user=User.objects.create_user(username, email, password)
        my_user.save()
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
        context={
            'ca':ca
        }
    return render(request, 'profile.html',context)

@login_required(login_url='login')
def sell_art(request):
    if request.method=='POST':
        User=request.user
        artist = request.POST.get('artist')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('photo')
        catagory=request.POST.get('category')
        Artwork.objects.create(seller=User, artist=artist, title=title, description=description, image=image,catagory=catagory ,price=price)
        
        return redirect('home')
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
        context={
            'ca':ca
        }
    return render(request, 'sell_art.html',context)

def art(request, category=None):
    if category:
        artworks = Artwork.objects.filter(catagory=category)
    else:
        artworks = Artwork.objects.all()
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
    context = {
        'artworks': artworks,
        'ca':ca
    }
    return render(request, 'art.html', context)

def artwork_detail(request, id):
    art_detail = Artwork.objects.get(id=id)
   
    ca = Cart.objects.filter(user=request.user).count()
    context = {
        'art_detail': art_detail,
        'ca':ca
    }
    
    return render(request, 'art_detail.html', context)

def cart(request,id):
    user = request.user
    artwork = Artwork.objects.get(id=id)
    # check condition for artist can not buy their own art 
    
    own_art  = artwork.seller == user
    if own_art:
        messages.warning(request, "You can not buy your own art.")
        return redirect('art_all')
    
    # Check if the same product exists in the cart for the current user
    cart_item_exists = Cart.objects.filter(user=user,art__id =id).exists()
    if cart_item_exists:
        messages.warning(request, "Item already in the cart.")
    else:
        # If the item is not in the cart, add it
        Cart.objects.create(user=user, art=artwork)
        messages.success(request, "Item added to the cart successfully.")
    return redirect('show_cart')

def show_cart(request):
    user = request.user
    data  = Cart.objects.filter(user=user)
    total = 0
    for p in data:
        value = p.quantity * p.art.price
        total = total + value
    totalamount = total + 40
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
    context = {
        'data': data ,
        'totalamount': totalamount,
        'total': total,
        'ca':ca
    }
    return render(request, 'cart.html', context)

def removecart(request):
    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(art=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        data = cart.objects.filter(user=user)
        total = 0
        for p in data:
            value = p.quantity * p.art.price
            total = total + value
        totalamount = total + 40
        data = {

            'total': total,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    

def add_address(request):
    if request.method == 'POST':
        
        user = request.user

        name = request.POST.get('name')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        zipcode = request.POST.get('zipcode')
        state = request.POST.get('state')
        Address.objects.create(
            user=user,
            name=name,
            locality=locality,
            city=city,
            mobile=mobile,
            zipcode=zipcode,
            state=state
        )
        
        return redirect('show_address')

    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
        context={
            'ca':ca
        }
    return render(request, 'add_address.html',context)

def show_address(request):
    user = request.user
    add = Address.objects.filter(user=user)
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
    context = {
        'add': add,
        'ca':ca
    }
    return render(request, 'show_address.html', context)

def delete_address(request, id):
    add = Address.objects.get(id=id)
    add.delete()
    return redirect('show_address')

def checkout(request):
    data = Cart.objects.filter(user=request.user)
    total = 0
    for p in data:
        value = p.quantity * p.art.price
        total = total + value
    totalamount = total + 40
    add = Address.objects.filter(user=request.user)
    
    # for razorpay
    razoramount = int(totalamount * 100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    k = {'amount': razoramount, "currency": 'INR', "receipt": "order_rcptid_12"}
    paymant_response = client.order.create(data=k)

    print(paymant_response)

    # {'id': 'order_Nxy2kh60XCMBJz', 'entity': 'order', 'amount': 416100, 'amount_paid': 0, 'amount_due': 416100, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1712980910}
    order_id = paymant_response['id']
    order_status = paymant_response['status']
    if order_status == 'created':
        pay = Payment(
            user=request.user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
        )
        pay.save()
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
    context = {
        'data': data,
        'totalamount': totalamount,
        'add': add,
        'total': total,
        'razoramount':razoramount,
        'order_id':order_id,
        'ca':ca
    }
    return render(request, 'checkout.html', context)

def paymentdone(request):
    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    cust_id = request.GET.get("cust_id")
    print(order_id, payment_id, cust_id)
    user = request.user
    add = Address.objects.get(id=cust_id)

    pay = Payment.objects.get(razorpay_order_id=order_id)
    pay.paid = True
    pay.razorpay_payment_id = payment_id
    pay.save()
    data = Cart.objects.filter(user=request.user)
    print(data)
    for i in data:
        Order(user=user, address=add, product=i.art, quantity=i.quantity, payment=pay).save()
        

    for c in data:
   
        c.delete()

    return redirect('order')


def order(request):
    op = Order.objects.filter(user=request.user)
    print(op)
    if request.user.is_authenticated:
        ca = Cart.objects.filter(user=request.user).count()
    context = {
        'order': op,
        'ca':ca
    }
    return render(request, 'order.html', context)

def receiveorder(request):
    received_orders = Order.objects.filter(product__seller=request.user)
    print(received_orders)
    context = {
        'receives': received_orders
    }
    # print(recive)
    return render(request, 'recive_order.html', context)

def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return redirect('receiveorder')
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})