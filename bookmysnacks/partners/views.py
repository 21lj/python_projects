from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from bmsAdmin.models import Login, Theater, Location
from .models import Shop, Category, Snacks, OrderDetail, Orders
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import os
from django.conf import settings
from django.db.models import Sum, F
import qrcode
import base64
from io import BytesIO


def hello(request):
    return render(request, 'partners/index.html')

def redirect2TheaterLogin(request):
    return render(request, 'partners/theater/login.html') 

def redirect2TheaterRegister(request):
    return render(request, 'partners/theater/register.html')

def redirect2ShopLogin(request):
    return render(request, 'partners/shops/login.html')

# def registerAsTheater(request):
#     if request.method == 'POST':
#         theater_name = request.POST.get('theater_name')
#         username = request.POST.get('username')
#         contact = request.POST.get('contact')
#         location = request.POST.get('location')
#         about = request.POST.get('about')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         theater_image = request.FILES.get('image')

#         locationRef = Location.objects.get(id=location) 

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return redirect('register')

#         # Create and save the Login instance
#         login = Login(username=username, password=password, role='theater')
#         login.save()

#         # Create and save the Theater instance
#         theater = Theater(
#             login=login,
#             theater_name=theater_name,
#             image=theater_image,  # Directly assign the uploaded image
#             contact=contact,
#             location=locationRef,
#             about=about,
#         )
#         theater.save()

#         messages.success(request, "Theater registered successfully!")
#         return redirect('partners:login')
#     locations = Location.objects.all()
#     return render(request, 'partners/theater/register.html', {'locations': locations})


def registerAsTheater(request):
    if request.method == 'POST':
        theater_name = request.POST.get('theater_name')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        location_id = request.POST.get('location')
        about = request.POST.get('about')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        theater_image = request.FILES.get('image')

        
        try:
            locationRef = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            messages.error(request, "Selected location does not exist.")
            return redirect('register')

        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        
        login = Login(username=username, password=password, role='theater')
        login.save()

        # Create and save the Theater instance
        theater = Theater(
            login=login,
            theater_name=theater_name,
            image=theater_image,  
            contact=contact,
            location=locationRef,
            about=about,
        )
        theater.save()

        messages.success(request, "Theater registered successfully!")
        return redirect('partners:login')

    
    locations = Location.objects.all()
    return render(request, 'partners/theater/register.html', {'locations': locations})


def theaterLog(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Login.objects.get(username=username)
            if user.check_password(password):
                user.last_login = timezone.now()  # Update last login
                user.save()  
                login(request, user)  # Log the user in
                return redirect('partners:home')  # Redirect to the home page
            else:
                error_message = "Invalid Password"
        except Login.DoesNotExist:
            error_message = "Invalid Username"

    return render(request, 'partners/theater/login.html', {'error_message': error_message})




@login_required
def theaterHome(request):
    return render(request, 'partners/theater/home.html', {'active_page': 'dashboard'})


@login_required
def theaterLogOut(request):
    logout(request)
    return redirect('partners:login')

@login_required
def shopAdminLogOut(request):
    logout(request)
    return redirect('partners:shopLogin')


@login_required
def regsterShops(request):
    login_instance = request.user  
    theater = get_object_or_404(Theater, login=login_instance)

    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        shop_image = request.FILES.get('shop_image')

        if password != confirm_password:
            return HttpResponse("<script>alert('Passwords do not match.')</script>")

        try:
            logShopInstance = Login(
                username=username,
                password=password,  
                role="shop"
            )
            logShopInstance.save()  

            shop = Shop(
                login=logShopInstance,
                theater=theater,
                shop_name=shop_name,
                email=email,
                phone=phone,
                shop_image=shop_image
            )
            shop.save()  

            messages.success(request, "Shop registered successfully!")
            return redirect('partners:manageShops')  

        except Exception as e:
            messages.error(request, str(e))  
            return HttpResponse("<script>alert('An error occurred.')</script>")
    # return render(request, 'partners/theater/shopRegister.html')
    return render(request, 'partners/theater/home.html', {'active_page': 'register_shop'})

def shopLog(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Login.objects.get(username=username, role="shop")
            if user.check_password(password):
                user.last_login = timezone.now()  
                user.save()  
                login(request, user)  
                return redirect('partners:manage-orders')  
            else:
                messages.error(request, "Invalid Password")
        except Login.DoesNotExist:
            messages.error(request, "Invalid Username")

    return render(request, 'partners/shops/login.html')  

def theaterProfile(request):
    user = request.user
    theater = get_object_or_404(Theater, login=user)
    location = get_object_or_404(Location, id=theater.location.id)

    content = {
        'tuser': theater,
        'loc': location,
        'active_page': 'profile'
    }
    return render(request, 'partners/theater/home.html', content)

# theater other functions

def contactShop(request):
    user = request.user
    theater_id = get_object_or_404(Theater, login=user)
    shops = Shop.objects.filter(theater_id=theater_id)

    shop_data = []
    for shop in shops:
        contact_info = f"Email: {shop.email}\nPhone: {shop.phone}"

        qr = qrcode.make(contact_info)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        shop_data.append({
            'shop': shop,
            'qr_code': img_str
        })

    context = {
        'active_page': 'contact',
        'shop_data': shop_data
    }
    return render(request, 'partners/theater/home.html', context)

def listRevenue(request):
    user = request.user
    theater = get_object_or_404(Theater, login=user)

    # Get all shops under this theater
    shops = Shop.objects.filter(theater=theater)

    # Get all snacks that belong to any shop in this theater
    snacks = OrderDetail.objects.filter(
    shop__in=shops,
    order__payment__payment_status="Completed"
).annotate(
    snack_name=F('snack__snack_name'),
    image=F('snack__image'),
    shop_name=F('shop__shop_name'),
    subtotal=F('quantity') * F('snack__price')
).values(
    'snack__id',
    'snack_name',
    'image',
    'shop_name'
).annotate(
    total_quantity=Sum('quantity'),
    total_revenue=Sum('subtotal')
)


    context = {
        'snacks': snacks,
        'theater': theater,
        'active_page': 'revenue'
    }
    return render(request, 'partners/theater/home.html', context)


# ________________________________

def idkk(request):
    return render(request, 'partners/shops/home.html', {'active_page': 'profile'})

def manageShops(request):
    user = request.user
    theater_id = get_object_or_404(Theater, login=user)

    shops = Shop.objects.filter(theater_id=theater_id)  
    #return render(request, 'partners/theater/manageShops.html', {'shops': shops})
    return render(request, 'partners/theater/home.html', {'shops': shops, 'active_page': 'manage'})


@login_required
def addSnacks(request):
    category = Category.objects.all()
    loginObj = request.user
    shop_id = get_object_or_404(Shop, login=loginObj)

    if request.method == 'POST':
        snack_name = request.POST.get('snack_name')
        category_id = request.POST.get('category_id')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        availability = request.POST.get('availability') == 'on'

        category = Category.objects.get(id=category_id)

        Snacks.objects.create(
            shop_id=shop_id,
            category_id = category,
            snack_name = snack_name,
            price=price,
            image=image,
            description=description,
            availability=availability
        )

        messages.success(request, "Snack Successfully Inserted.")
        return redirect('partners:manageSnacks')
    
    content = {
        'active_page': 'add_snacks',
        'categories': category
    }
    return render(request, 'partners/shops/home.html', content)

@login_required
def manageSnacks(request):
    loginObj = request.user
    shop_id = get_object_or_404(Shop, login=loginObj)
    snacks_list = Snacks.objects.filter(shop_id=shop_id)
    content = {
        'snacks': snacks_list,
        'active_page': 'manage'
    }
    return render(request, 'partners/shops/home.html', content)


def deleteSnacks(request, sId):
    if request.method == 'POST':
        snack = get_object_or_404(Snacks, id=sId)

        if snack.image:
            old_image_path = os.path.join(settings.MEDIA_ROOT, str(snack.image))
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        snack.delete()
        messages.success(request, "Snack deleted successfully.")
        return redirect('partners:manageSnacks')
    
def deleteShop(request, spId):
    if request.method == 'POST':
        shop = get_object_or_404(Shop, id=spId)

        if shop.shop_image:
            old_image_path = os.path.join(settings.MEDIA_ROOT, str(shop.shop_image))
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        shop.delete()
        messages.success(request, "Shop deleted successfully.")
        return redirect('partners:manageShops')
    


def editSnacks(request, sId):
    snack = get_object_or_404(Snacks, id=sId)
    categories = Category.objects.all()

    if request.method == 'POST':
        snack_name = request.POST.get('snack_name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        availability = request.POST.get('availability') == 'on'
        category_id = request.POST.get('category_id')
        image = request.FILES.get('image')

      
        snack.snack_name = snack_name
        snack.price = price
        snack.description = description
        snack.availability = availability
        snack.category_id = Category.objects.get(id=category_id)

        
        if image:
            if snack.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(snack.image))
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

           
            snack.image = image

        snack.save()  
        return redirect('partners:manageSnacks')  

    content = {
        'snack': snack,
        'categories': categories
    }
    
    return render(request, 'partners/shops/editSnacks.html', content)

def shopProfile(request):
    user = request.user
    shopId = get_object_or_404(Shop, login=user)
    myShop = Shop.objects.get(id=shopId.id)
    content = {
        'suser': myShop,
        'active_page': 'profile'
    }
    return render(request, 'partners/shops/home.html', content)

def editShopProfile(request):
    user = request.user
    shopId = get_object_or_404(Shop, login=user)
    myShop = Shop.objects.get(id=shopId.id)

    if request.method == 'POST':
        shop_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')

        myShop.shop_name = shop_name
        myShop.email = email
        myShop.phone = phone

        if image:
            if  myShop.shop_image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(myShop.shop_image))
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

           
            myShop.shop_image = image
        myShop.save()
        return redirect('partners:shopProfile')

    return render(request, 'partners/shops/editprofile.html', {'shop': myShop})

def editTheaterProfile(request):
    user = request.user
    theater = get_object_or_404(Theater, login=user)
    myTheater = Theater.objects.get(id=theater.id)
    location = get_object_or_404(Location, id=theater.location.id)

    if request.method == 'POST':
        theater_name = request.POST.get('fullname')
        #location = request.POST.get('location')
        contact = request.POST.get('contact')
        about = request.POST.get('about')
        image = request.FILES.get('image')

        myTheater.theater_name = theater_name
        #myTheater.location = location
        myTheater.about = about
        myTheater.contact = contact 

        if image:
            if myTheater.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(myTheater.image))
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

            myTheater.image = image
            
        myTheater.save()
        return redirect('partners:profile')

    return render(request, 'partners/theater/editprofile.html', {'theater': myTheater, 'loc':location})

# +++++++++++> response to orders <+++++++++++


def accept_order(request, order_id):

    order = get_object_or_404(Orders, id=order_id)

    order.is_accepted = True
    order.order_status = "Ready"
    order.save()

    messages.success(request, f"Order {order.unique_order_id} has been accepted.")
    return redirect("partners:view-orders")  

def reject_order(request, order_id):
    order = get_object_or_404(Orders, id=order_id)

    
    order.order_status = "Rejected"
    order.save()

    messages.error(request, f"Order {order.unique_order_id} has been rejected.")
    return redirect("partners:view-orders")  


def manageOrders(request):
    shop = request.user.shop 
    orders = Orders.objects.filter(order_details__shop=shop, order_status="Pending").distinct()

    orders_data = []
    
    for order in orders:
        order_items = OrderDetail.objects.filter(order=order, shop=shop)

        snacks_list = [
            {
                "snack_name": item.snack.snack_name,
                "quantity": item.quantity,
                "price": item.snack.price
            }
            for item in order_items
        ]

        orders_data.append({
            "order": order,
            "snacks": snacks_list,
            "user": order.user  
        })

    content = {
        "orders_data": orders_data,
        "active_page": "manage-orders",
    }

    return render(request, "partners/shops/home.html", content)


# +++++++++++> response to orders <+++++++++++


def viewOrders(request):
    user = request.user
    shop = get_object_or_404(Shop, login=user)
    # orders = OrderDetail.objects.filter(shop=shop)
    orders = Orders.objects.filter(order_details__shop=shop).distinct()
    order_items = [(order, OrderDetail.objects.filter(order=order)) for order in orders]


    content = {
        'active_page': 'view-orders',
        'orders': orders,
        'order_items': order_items
    }
    return render(request, 'partners/shops/home.html', content)


def trackRevenue(request):
    shop = request.user.shop

    order_details = OrderDetail.objects.filter(
        order__payment__payment_status="Completed",
        shop=shop
    ).annotate(
        total_price=F('quantity') * F('snack__price')
    )

    total_revenue = order_details.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    total_items_sold = order_details.aggregate(total_items=Sum('quantity'))['total_items'] or 0

    # Group by snack and collect buyers directly from order_details
    snack_stats = order_details.values('snack__id', 'snack__snack_name').annotate(
        items_sold=Sum('quantity'),
        revenue=Sum('total_price')
    )

    snack_data = []
    for snack in snack_stats:
        buyers = order_details.filter(snack__id=snack['snack__id']).values(
            'order__user__login__username',  
            'order__user__email'
        ).distinct()

        # print(buyers)

        snack_data.append({
            'snack_name': snack['snack__snack_name'],
            'items_sold': snack['items_sold'],
            'revenue': snack['revenue'],
            'buyers': list(buyers)
        })

    content = {
        "total_revenue": total_revenue,
        "total_items_sold": total_items_sold,
        "snack_stats": snack_data,
        'active_page': 'revenue'
    }

    return render(request, 'partners/shops/home.html', content)