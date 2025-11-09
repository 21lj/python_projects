from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from bmsAdmin.models import Login, User, Location
from partners.models import Theater, Shop, Snacks, Orders, OrderDetail, Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import os, random, json
from collections import defaultdict
from django.conf import settings
from django.db import transaction


def userSignUp(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('bmsUsers:register')
        
        newUserLogin = Login(username=username, password=password, role='user')
        newUserLogin.save()

        if not image:
            image = f"{settings.STATIC_URL}images/default_pic.jpg"


        newUser = User(
            login_id = newUserLogin.id,
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            image=image
        )

        newUser.save()
        messages.success(request, f"{username} registered successfully!")
        return redirect('bmsUsers:register')



    return render(request, 'bmsUsers/register.html')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Login.objects.get(username=username, role="user")
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save()  
                login(request, user) 
                return redirect('bmsUsers:page1')  
            else:
                messages.error(request, "Invalid Password")
        except Login.DoesNotExist:
            messages.error(request, "Invalid Username")


    return render(request, 'bmsUsers/login.html')

def userLogOut(request):
    logout(request)
    return redirect('bmsUsers:login')

def landing(request):
    location = Location.objects.all()
    theater = None

    if request.method == 'POST':
        location_id = request.POST.get('location_id')
        theater = Theater.objects.filter(location=location_id)
        location = None
    if request.method == 'GET' and 'theaters' in request.GET:
        theater_id = request.GET.get('theaters')
        #print(theater_id)
        return redirect("bmsUsers:home", tid=theater_id)
    content = {
        'locations': location,
        'theaters': theater
    }
    return render(request, 'bmsUsers/landingpage.html', content)

# ++++++++++> Testing User functionalities <++++++++++


# def getBasicInfo(tid, user_id):
#     currentUser = User.objects.get(id=user_id)
#     getTheater = Theater.objects.get(id=tid)
#     location = get_object_or_404(Location, id=getTheater.location.id)
#     #location = Location.objects.get(id=getTheater.location)
#     getShops = Shop.objects.filter(theater_id=tid)
#     infos = {
#         'userLogged': currentUser,
#         'theater': getTheater,
#         'location': location,
#         'shops': getShops,
#     }

    
#     return infos

def getBasicInfo(tid, user_id):
    currentUser = User.objects.get(id=user_id)
    getTheater = Theater.objects.get(id=tid)
    location = get_object_or_404(Location, id=getTheater.location.id)
    
    # Get all shops for the theater
    getShops = Shop.objects.filter(theater_id=tid)
    
    # Create a list of shops with their corresponding snacks
    shops_with_snacks = []
    for shop in getShops:
        snacks_list = Snacks.objects.filter(shop_id=shop.id)  # Filter snacks for each shop
        shops_with_snacks.append({
            'shop': shop,
            'snacks': snacks_list
        })
    
    infos = {
        'userLogged': currentUser,
        'theater': getTheater,
        'location': location,
        'shops': shops_with_snacks,  # Include shops with their snacks
    }
    
    return infos



def home(request, tid):
    # print(tid)
    loginObj = request.user
    user_id = get_object_or_404(User, login=loginObj)
    content = getBasicInfo(tid, user_id.id)
    request.session['theaterLoggedByUser'] = tid
    request.session['userInfo'] = user_id.id
    return render(request, 'bmsUsers/home.html', content)

def shopFun(request, sid):
    snacks = Snacks.objects.filter(shop_id=sid)
    shop = Shop.objects.get(id=sid)
    content = {
        'snacks': snacks,
        'shop': shop
    }
    return render(request, 'bmsUsers/snackshop.html', content)

def getSnacks(request, snackId):
    snack = Snacks.objects.get(id=snackId)
    shop = snack.shop_id
    simlarSnacks = Snacks.objects.filter(shop_id=shop).exclude(id=snackId)[:2]
    content = {
        'snack': snack,
        'simlarSnacks': simlarSnacks
        }
    return render(request, 'bmsUsers/snackdetails.html', content)



# def myOrders(request):
#     userId = request.session.get('userInfo')
#     # orders = Orders.objects.filter(user=userId)
#     # orderDetails = OrderDetail.objects.filter(order=orders)
#     # snack = Snacks.objects.get(id=orderDetails.snack)
#     # content = {
#     #     'orders': orders,
#     #     'userId': userId
#     #     }

#     orders = Orders.objects.filter(user=userId)
    
    
#     order_info = []
#     for order in orders:
#         details = OrderDetail.objects.filter(order=order)
#         for detail in details:
#             try:
#                 snack = Snacks.objects.get(id=detail.snack.id)
#                 order_info.append({
#                     'order_id': order.id,
#                     'snack_name': snack.snack_name,
#                     'quantity': detail.quantity,
#                     'price': snack.price,
#                     'status': order.payment_status,
#                     'order_uid': order.unique_order_id,
#                     'order_status': order.order_status

#                 })
#             except Snacks.DoesNotExist:
#                 order_info.append({
#                     'order_id': order.id,
#                     'snack_name': 'Snack not found',
#                     'quantity': detail.quantity,
#                     'price': snack.price,
#                 })

#     content = {
#         'order_info': order_info,
#         'userId': userId
#     }
#     return render(request, 'bmsUsers/myOrders.html', content)


def myOrders(request):
    userId = request.session.get('userInfo')

    orders = Orders.objects.filter(user=userId).order_by('-created_at')

    order_info = []
    grouped_orders = defaultdict(list)  #  Dictionary to group cart orders

    for order in orders:
        details = OrderDetail.objects.filter(order=order)
        
        for detail in details:
            try:
                snack = Snacks.objects.get(id=detail.snack.id)
                order_data = {
                    'order_id': order.id,
                    'snack_name': snack.snack_name,
                    'quantity': detail.quantity,
                    'price': snack.price,
                    'status': order.payment_status,
                    'order_uid': order.unique_order_id,
                    'order_status': order.order_status
                }

                #  If cart order, group it under the same order UID
                if order.unique_order_id in grouped_orders:
                    grouped_orders[order.unique_order_id].append(order_data)
                else:
                    grouped_orders[order.unique_order_id] = [order_data]

            except Snacks.DoesNotExist:
                order_info.append({
                    'order_id': order.id,
                    'snack_name': 'Snack not found',
                    'quantity': detail.quantity,
                    'price': 0
                })

    #  Convert grouped cart orders into a single order record
    for order_uid, items in grouped_orders.items():
        if len(items) > 1:  #  If multiple items, show as "Cart Order"
            total_price = sum(item['price'] * item['quantity'] for item in items)
            order_info.append({
                'order_id': items[0]['order_id'],  # Use first order ID
                'snack_name': f"Cart Order ({len(items)} items)",  #  Display as Cart Order
                'quantity': "-",
                'price': total_price,
                'status': items[0]['status'],
                'order_uid': order_uid,
                'order_status': items[0]['order_status'],
                'is_cart': True  #  Mark as cart order
            })
        else:
            order_info.append(items[0])  #  Show single-item orders normally

    content = {
        'order_info': order_info,
        'userId': userId
    }
    return render(request, 'bmsUsers/myOrders.html', content)

# --------------------> Add to Cart Feature <--------------------

def viewCartOrders(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    details = OrderDetail.objects.filter(order=order)

    cart_items = []
    for detail in details:
        cart_items.append({
            'snack_name': detail.snack.snack_name,
            'quantity': detail.quantity,
            'price': detail.snack.price,
            'image': detail.snack.image,
            'subtotal': (detail.quantity * detail.snack.price)
        })

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    content = {
        'cart_items': cart_items,
        'total_price': total_price,
        'order_uid': order.unique_order_id,
        }

    return render(request, 'bmsUsers/viewCartOrders.html', content)


def add2Cart(request, snack_id):
    quantity = request.POST.get('quantity')

    if isinstance(quantity, str):
        quantity = int(quantity)

    if quantity is None:
        quantity = 1
    
    user = get_object_or_404(User, login=request.user)
    snack = get_object_or_404(Snacks, id=snack_id)

    

    cart = user.cart or {"snacks": []}  

    # Check if the snack is already in the cart
    for item in cart["snacks"]:
        if item["snack_id"] == snack_id:
            item["quantity"] += 1  
            break
    else:
        cart["snacks"].append({"snack_id": snack_id, "quantity": quantity})  

    user.cart = cart
    user.save()

    messages.success(request, f"{snack.snack_name} added to cart!")
    return redirect("bmsUsers:cart")


def viewCart(request):
   
    user = get_object_or_404(User, login=request.user)
    cart_items = user.cart.get("snacks", [])

    snacks = []
    total_price = 0

    for item in cart_items:
        snack = get_object_or_404(Snacks, id=item["snack_id"])
        snacks.append({
            "id": snack.id,
            "name": snack.snack_name,
            "price": snack.price,
            "quantity": item["quantity"],
            "subtotal": snack.price * item["quantity"]
        })
        total_price += snack.price * item["quantity"]

    return render(request, "bmsUsers/cart.html", {"snacks": snacks, "total_price": total_price})


def cartDetailsPush2Orders(request):
    user = get_object_or_404(User, login=request.user)
    cart_items = user.cart.get("snacks", [])

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("bmsUsers:cart")

    total_price = sum(
        get_object_or_404(Snacks, id=item["snack_id"]).price * item["quantity"]
        for item in cart_items
    )

    with transaction.atomic():
        order = Orders.objects.create(
            user=user,
            order_status="Pending",
            total_price=total_price,
            payment_status="Pending"
        )

        for item in cart_items:
            snack = get_object_or_404(Snacks, id=item["snack_id"])
            OrderDetail.objects.create(
                order=order,
                snack=snack,
                shop=snack.shop_id,
                quantity=item["quantity"]
            )

        # Store order ID in session instead of full order data
        request.session["pending_order_id"] = order.id
        request.session.modified = True

        # Clear cart after storing order ID
        user.cart = {"snacks": []}
        user.save()

    messages.success(request, f"Order {order.unique_order_id} placed successfully!")
    return redirect("bmsUsers:process_payment")


# --------------------> Add to Cart Feature <--------------------

# ********************>Payment<********************


def buy_now(request, sid):
    user = get_object_or_404(User, login=request.user)
    snack = get_object_or_404(Snacks, id=sid)
    quantity = request.POST.get('quantity')

    if isinstance(quantity, str):
        quantity = int(quantity)

    if quantity is None:
        quantity = 1

    
    total_price = snack.price * quantity

    # Create & Save Order before storing in session
    order = Orders.objects.create(
        user=user,
        order_status='Pending',
        total_price=total_price,
        payment_status='Pending'
    )

    # Create OrderDetail
    OrderDetail.objects.create(
        order=order,
        snack=snack,
        quantity=quantity,
        shop=snack.shop_id
    )

    # Store only `order.id` in session instead of raw order data
    request.session["pending_order_id"] = order.id
    request.session.modified = True

    return redirect("bmsUsers:process_payment")


def processPayment(request):

    order_id = request.session.get("pending_order_id")
    if not order_id:
        messages.error(request, "No order found.")
        return redirect("bmsUsers:myorders")

    order = get_object_or_404(Orders, id=order_id)
    order_items = OrderDetail.objects.filter(order=order)

    # Calculate subtotal and total price
    total_price = 0
    updated_order_items = []

    for item in order_items:
        subtotal = item.snack.price * item.quantity
        total_price += subtotal  # Add to total price

        updated_order_items.append({
            "snack": item.snack,
            "quantity": item.quantity,
            "price": item.snack.price,
            "subtotal": subtotal  # Now subtotal is included
        })

    order.total_price = total_price  # Ensure order has correct total price
    order.save()

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        transaction_id = str(random.randint(1000000000, 9999999999))

        with transaction.atomic():
            if payment_method == 'Cash on Delivery':
                order.payment_status = "Completed/COD"
            else:
                order.payment_status = "Completed"
            order.order_status = "Pending"
            order.save()

            Payment.objects.create(
                order=order,
                user=order.user,
                amount=total_price,  # Using correctly calculated total price
                payment_method=payment_method,
                payment_status="Completed",
                transaction_id=transaction_id
            )

        messages.success(request, f"Payment successful! Transaction ID: {transaction_id}")

        del request.session["pending_order_id"]
        request.session.modified = True

        return redirect("bmsUsers:notify_order_confirmation", order_id=order.id)

    return render(request, "bmsUsers/orderConfirmation.html", {
        "order": order, 
        "order_items": updated_order_items,  # Now order_items contains subtotal
        "total_price": total_price  # Correct total price
    })


def notifyOrderConfirmation(request, order_id):

    order = get_object_or_404(Orders, id=order_id)

    return render(request, "bmsUsers/notifyOrder.html", {"order": order})


# ********************>Payment<********************


# ....................>Edit User Profile<....................

def profile(request):
   # theaterId = request.session.get('theaterLoggedByUser')
    user = get_object_or_404(User, login=request.user)
    content = {
        'curentUser': user,
        }
    return render(request, 'bmsUsers/profile.html', content)

def editUserProfile(request):
    user = request.user
    user_profile = get_object_or_404(User, login=user)

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        contact = request.POST.get('phone')
        email = request.POST.get('email')
        image = request.FILES.get('image')

        user_profile.fname = first_name
        user_profile.lname = last_name
        user_profile.phone = contact
        user_profile.email = email

        if image:
            if user_profile.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.image))
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
            user_profile.image = image
            
        user_profile.save()
        return redirect('bmsUsers:profile')  # Change to your profile URL name

    return render(request, 'bmsUsers/edit-user-pf.html', {'profile': user_profile})