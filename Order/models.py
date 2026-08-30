from django.contrib.auth.models import User
from django.db import models
from Products.models import Product

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

PAYMENT_STATUS_CHOICES = (
    ('Unpaid', 'Unpaid'),
    ('Paid', 'Paid'),
    ('Failed', 'Failed'),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField()
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=15)
    phone_no = models.CharField(max_length=11)
    payment_method = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} (Order #{self.id}) - {self.payment_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}: {self.order.full_name}"