from django.db import models
from bmsAdmin.models import Login, Theater, User
import random

class Shop(models.Model):  
    login = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='shop')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shops')  
    shop_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255) 
    phone = models.CharField(max_length=20)  
    shop_image = models.ImageField(upload_to='shops/')

    def __str__(self):
        return self.shop_name  

class Category(models.Model):
    category_name = models.CharField(max_length=25)

    def __str__(self):
        return self.category_name

class Snacks(models.Model):
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='snacks')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='snacks')
    snack_name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='snacks/')
    description = models.CharField(max_length=150)
    availability = models.BooleanField(default=True)
    
    def __str__(self):
        return self.snack
    

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    unique_order_id = models.CharField(max_length=8, unique=True, editable=False)
    order_status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=15, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, default="Pending")
    is_accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.unique_order_id:
            self.unique_order_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            unique_id = str(random.randint(10000000, 99999999))  # Consider a more robust method
            if not Orders.objects.filter(unique_order_id=unique_id).exists():
                return unique_id

class OrderDetail(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_details')
    snack = models.ForeignKey(Snacks, on_delete=models.CASCADE, related_name='order_details')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_details')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.snack.name} in Order {self.order.unique_order_id}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('UPI', 'UPI'),
        ('Paytm', 'Paytm'),
        ('Net Banking', 'Net Banking'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    order = models.OneToOneField(Orders, on_delete=models.CASCADE, related_name='payment')  # Each order has one payment
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS, default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  # For tracking online payments
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.unique_order_id} - {self.payment_status}"
