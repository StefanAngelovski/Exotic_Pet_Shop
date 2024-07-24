from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Store.forms import RegistrationForm
from Store.models import *
from django.contrib import messages


# Create your views here.
def display_index(request):
    animals = Animal.objects.all()
    animal_count = animals.count()
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.cart is None:  # Check if the user_profile has an associated cart
        user_profile.cart = Cart.objects.create(user=request.user)
        user_profile.save()
    cart_items = user_profile.cart.cart_items.all()  # Get the cart items for the current user

    # Calculate the total price for each cart item
    for cart_item in cart_items:
        cart_item.total_price = cart_item.animal.price * cart_item.quantity

    cart = user_profile.cart  # Get the cart for the current user
    return render(request, 'index.html',
                  {'animals': animals, 'animal_count': animal_count, 'cart_items': cart_items, 'cart': cart})


def display_about(request):
    return render(request, 'about.html')


def display_contact(request):
    return render(request, 'contact.html')


def display_cart(request):
    return render(request, 'cart.html')


def display_userProfile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'userProfile.html', {'user': user, 'user_profile': user_profile})


def display_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('Store:userProfile')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['fullName']
        user.email = request.POST['email']
        user.save()

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.phone = request.POST['phone']
        user_profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('Store:userProfile')
    else:
        return redirect('Store:userProfile')


@login_required
def update_shipping_details(request):
    if request.method == 'POST':
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.shipping_name = request.POST['shippingName']
        user_profile.shipping_address = request.POST['shippingAddress']
        user_profile.shipping_city = request.POST['shippingCity']
        user_profile.shipping_state = request.POST['shippingState']
        user_profile.shipping_zip = request.POST['shippingZip']
        user_profile.save()
        messages.success(request, 'Shipping details updated successfully')
        return redirect('Store:userProfile')
    else:
        return redirect('Store:userProfile')


def display_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('Store:userProfile')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('Store:login')
    else:
        return render(request, 'login.html')


def display_animal(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    return render(request, 'animalInformation.html', {'animal': animal})


def add_to_cart(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    cart = request.user.userprofile.cart
    if cart is None:
        cart = Cart.objects.create(user=request.user)
        request.user.userprofile.cart = cart
        request.user.userprofile.save()
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        cart_item = CartItem(animal=animal, quantity=quantity, age=age, sex=sex)
        cart_item.save()
        cart.cart_items.add(cart_item)
        # Update the total price of the cart
        cart.total_price += animal.price * quantity
        cart.save()
    return redirect('Store:index')
