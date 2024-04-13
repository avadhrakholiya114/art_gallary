from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
import razorpay

from .models import Artwork,Cart,Address,Payment,Orderplaced
from django.contrib import messages
from django.db.models import Q


from django.conf import settings
# Create your views here.
# //artist 123
def home(request):
    return render(request, 'index.html')

def  about(request):
    return render(request, 'about.html')

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
    return render(request, 'profile.html')

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
        
    return render(request, 'sell_art.html')

def art(request, category=None):
    if category:
        artworks = Artwork.objects.filter(catagory=category)
    else:
        artworks = Artwork.objects.all()
    context = {
        'artworks': artworks
    }
    return render(request, 'art.html', context)

def artwork_detail(request, id):
    art_detail = Artwork.objects.get(id=id)
    context = {
        'art_detail': art_detail
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
    context = {
        'data': data ,
        'totalamount': totalamount,
        'total': total,
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
    
    return render(request, 'add_address.html')

def show_address(request):
    user = request.user
    add = Address.objects.filter(user=user)
    context = {
        'add': add
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
    
    context = {
        'data': data,
        'totalamount': totalamount,
        'add': add,
        'total': total,
        'razoramount':razoramount,
        'order_id':order_id
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
 
    for c in data:
        Orderplaced(user=user, address=add, product=c.art, quantity=c.quantity, payment=pay).save()
        c.delete()
    return redirect('show_cart')