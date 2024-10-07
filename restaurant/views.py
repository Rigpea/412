# restaurant/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import datetime


# Create your views here.

cuban = 5
pulled = 2
orange = 3
loaded = 10


def main(request):
    context = {
        'image': 'https://static.wixstatic.com/media/b464e9_8b19172aff1d40cb839c7c922ca05916~mv2.jpg/v1/fill/w_980,h_735,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/I8k843rMguB8.jpg'
        }

    return render(request, 'restaurant/main.html', context)


def order(request):
    if request.method == "POST":
        # Gather form data
        name = request.POST.get("fname")
        items = request.POST.getlist("items")
        phone = request.POST.get("hname")
        email = request.POST.get("email")

        # Generate random ready time
        now = datetime.datetime.now()
        ready_time = now + datetime.timedelta(minutes=random.randint(30, 60))

        # Pass data to confirmation page
        return redirect('confirmation', {
            'name': name,
            'items': items,
            'ready_time': ready_time,
            'phone': phone,
            'email': email,
        })
    return render(request, 'restaurant/order.html')


def confirmation(request):
    # Generate a random ready time (between 30 and 60 minutes)
    now = datetime.datetime.now()
    ready_time = now + datetime.timedelta(minutes=random.randint(30, 60))

    menu_items = {
            'Cuban Sandwich $5': 5,
            'Pulled Pork Sandwich $2': 2,
            'Orange Chicken $3': 3,
            'Loaded Baked Potato $10': 10
        }

    # Retrieve any relevant data from the request or session
    items = request.POST.getlist('items')
    name = request.POST.get('fname')
    phone = request.POST.get('hphone')
    email = request.POST.get('hemail')
    special = request.POST.get('comments')

    total_price = sum([menu_items[item] for item in items if item in menu_items])
    context = {
            'name': name,
            'items': items,
            'total_price': total_price,
            'phone': phone,
            'email': email,
            'special_instructions': special,
            'ready_time': ready_time,
        }

    return render(request, 'restaurant/confirmation.html', context)