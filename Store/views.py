from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from Store.forms import RegistrationForm
from Store.models import *
from django.contrib import messages


# Create your views here.
def display_index(request):
    animals = Animal.objects.all()
    animal_count = animals.count()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    else:
        cart = None
        cart_items = []

    # Query for top-level categories (those without parents)
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('category_set')

    return render(request, 'index.html',
                  {'animals': animals, 'animal_count': animal_count, 'cart_items': cart_items, 'cart': cart,
                   'categories': categories})


def display_about(request):
    return render(request, 'about.html')


def display_contact(request):
    return render(request, 'contact.html')


@login_required
def display_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # Use the related_name 'items' we set in the CartItem model
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart': cart})


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
            # Create a cart
            Cart.objects.get_or_create(user=user)
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
            # Create a cart for the user if it doesn't exist
            Cart.objects.get_or_create(user=user)
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


@login_required
def add_to_cart(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        age = request.POST.get('age')
        sex = request.POST.get('sex')

        # Check if the item is already in the cart
        existing_item = cart.items.filter(animal=animal, age=age, sex=sex).first()

        if existing_item:
            # Update existing item
            existing_item.quantity += quantity
            existing_item.save()
        else:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                animal=animal,
                quantity=quantity,
                age=age,
                sex=sex
            )

        # Update the total price of the cart
        cart.total_price = sum(item.animal.price * item.quantity for item in cart.items.all())
        cart.save()

    return redirect('Store:index')
    #TODO add sex to selection


def search_animals(request):
    query = request.GET.get('query', '')
    animals = Animal.objects.filter(common_name__icontains=query)[:5]
    data = [{'id': animal.id, 'name': animal.common_name} for animal in animals]
    return JsonResponse(data, safe=False)
