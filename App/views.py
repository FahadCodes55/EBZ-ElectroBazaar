from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Item, User, ContactUs

import json
from django.http import JsonResponse
from google.auth.transport import requests
from google.oauth2 import id_token

# Create your views here.

def home(request):
    query = Item.objects.order_by()
    # If you have used for specific price , date use order_by('-field_name')[:2]
    return render(request, 'App/KidStore.html', {'items' : query})


def shop(request):
    query = Item.objects.all()
    return render(request, 'App/shop.html', {'items' : query})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Login successful! {user.username}" )
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'App/Authentication/login.html')

def logout(request):
        auth.logout(request)
        messages.info(request, "You have logged out successfully.")
        return redirect('/')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')

        else:
            messages.info(request, "Password Doesn't match")
            return redirect('register')

    else:
        return render(request, 'App/Authentication/register.html')

def success(request):
    return redirect('/')


def send_email(subject, message, recipient_list=None):
    # If you don't specify an email, it defaults to sending it to you!
    if recipient_list is None:
        recipient_list = [settings.EMAIL_HOST_USER]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email failed to send: {e}")
        return False


@login_required()
def contact_form(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_subject = request.POST.get('subject')
        user_message = request.POST.get('message')

        ContactUs.objects.create(
            name=user_name,
            email=user_email,
            subject=user_subject,
            message=user_message
        )

        admin_sub = f"New Contact Form Submission: {user_subject}"
        admin_msg = f"Name: {user_name}\nEmail: {user_email}\n\nMessage:\n{user_message}"

        send_email(admin_sub, admin_msg)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')

    return render(request, 'App/KidStore.html')


# Replace with your actual Client ID
GOOGLE_CLIENT_ID = "262691374238-jtlir0qo8et0gp86bnt04o19l4vch8e2.apps.googleusercontent.com"


def google_jwt_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("credential")

            # Securely verify the token signature
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GOOGLE_CLIENT_ID,
            )

            email = idinfo.get('email')
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': idinfo.get('given_name', ''),
                    'last_name': idinfo.get('family_name', '')
                }
            )

            auth.login(request, user)
            messages.success(request, f"Login successful! {user.username}")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)