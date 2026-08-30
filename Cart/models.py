from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# One step Check Product model


# Third Step / second step if pickable product already in cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Second Step
# for one cart can have many cart items
class CartItem(models.Model):
    product = models.ForeignKey('Products.Product', on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


    # when user hit add to cart first check if this item is already in cart so you preferred
    # increment Cart Model Used or if no available so add to cart goes to CartItem Model and
    # generate it a new product in CartItem so if user more buy products it stores in same Cart