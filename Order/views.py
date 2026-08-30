from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import stripe

from .models import Order, OrderItem
from Products.models import Product
from Cart.models import Cart, CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    # 1. CALCULATE EVERYTHING EXACTLY LIKE THE CART PAGE
    sub_total = sum(item.subtotal() for item in cart_items) if cart_items else 0
    tax = round(float(sub_total) * 0.05, 2)
    shipping = 10.0 if sub_total > 0 else 0.0
    discount = 0.0
    grand_total = round((float(sub_total) + tax + shipping) - discount, 2)

    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zip_code')
        phone = request.POST.get('phone_no')
        payment = request.POST.get('payment_method')

        # 2. SAVE THE GRAND TOTAL TO THE DATABASE, NOT JUST SUBTOTAL
        create_order = Order.objects.create(
            user=request.user,
            full_name=fullname,
            address=address,
            city=city,
            zip_code=zipcode,
            phone_no=phone,
            payment_method=payment,
            total_amount=grand_total  # UPDATED HERE
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=create_order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # --- STRIPE INTEGRATION ---
        if payment == 'stripe':
            try:
                success_url = request.build_absolute_uri(reverse(
                    'payment_success')) + f"?reference={create_order.pk}&stripe_session_id={{CHECKOUT_SESSION_ID}}"
                cancel_url = request.build_absolute_uri(reverse('payment_failed'))

                # Build line items for Stripe Checkout
                line_items = []
                for item in cart_items:
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': item.product.name,
                            },
                            'unit_amount': int(item.product.price * 100),
                        },
                        'quantity': item.quantity,
                    })

                # 3. ADD TAX & SHIPPING AS A SEPARATE STRIPE LINE ITEM
                if tax + shipping > 0:
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Tax & Shipping',
                            },
                            'unit_amount': int((tax + shipping) * 100),
                        },
                        'quantity': 1,
                    })

                # Create the Stripe Checkout Session
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=success_url,
                    cancel_url=cancel_url,
                    client_reference_id=str(create_order.pk),
                )

                return redirect(checkout_session.url, code=303)

            except Exception as e:
                create_order.delete()
                messages.error(request, f'Failed to connect to Stripe: {str(e)}')
                return redirect('checkout')

        #  CASH ON DELIVERY OR OTHER METHODS
        else:
            product_list = "\n".join(
                [f"- {item.quantity}x {item.product.name} (${item.product.price})" for item in cart_items])
            subject = f"Order Confirmed - Electro Bazaar #{create_order.id}"
            message = (
                f"Hello {request.user.username},\n\n"
                f"Thank you for shopping with us!\n\n"
                f"Your Cash on Delivery order for ${create_order.total_amount} has been successfully placed.\n\n"
                f"Items Ordered:\n{product_list}\n\n"
                f"You will pay this amount in cash when your items arrive at {create_order.address}, {create_order.city}.\n\n"
                f"We will notify you as soon as your items ship."
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed to send: {e}")

            cart_items.delete()
            messages.success(request, 'Your order has been created!')
            return redirect('order_success', pk=create_order.pk)

    # 4. PASS ALL CALCULATIONS TO THE CHECKOUT HTML
    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'tax': tax,
        'shipping': shipping,
        'grand_total': grand_total
    }
    return render(request, 'Order/checkout.html', context)


def payment_success(request):
    transaction_id = request.GET.get('stripe_session_id') or request.GET.get('tracker', 'N/A')
    order_pk = request.GET.get('reference') or request.GET.get('order_id')

    if order_pk:
        order = get_object_or_404(Order, pk=order_pk)

        if order.payment_status != 'Paid':
            order.payment_status = 'Paid'
            order.save()

            product_list = "\n".join([f"- {item.quantity}x {item.product.name}" for item in order.items.all()])

            subject = f"Payment Confirmation - Electro Bazaar #{order.id}"

            message = f"Hello {request.user.username},\n\nThank you for shopping with us!\n\nYour online payment of ${order.total_amount} was successful. \nTransaction ID: {transaction_id}\n\nItems Ordered:\n{product_list}\n\nWe will notify you as soon as your items ship."

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed to send: {e}")

            CartItem.objects.filter(cart__user=request.user).delete()

        context = {
            'transaction_id': transaction_id,
            'amount': order.total_amount,
            'date': timezone.now().strftime("%B %d, %Y"),
        }
        return render(request, 'Order/payment_success.html', context)


def payment_failed(request):
    order_pk = request.GET.get('reference') or request.GET.get('order_id')

    if order_pk:
        try:
            order = Order.objects.get(pk=order_pk)
            order.delete()
            print(f"Ghost Order #{order_pk} deleted successfully.")
        except Order.DoesNotExist:
            pass

    context = {
        'error_message': 'Your transaction was declined or cancelled.'
    }
    return render(request, 'Order/payment_failed.html', context)


def order_success(request, pk):
    order_id = get_object_or_404(Order, pk=pk)
    if order_id.user != request.user:
        return redirect('/')
    else:
        return render(request, 'Order/order_detail.html', {'order': order_id})