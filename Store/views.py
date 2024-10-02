from decimal import Decimal

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
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

    categories = Category.objects.all()  # Get all categories
    return render(request, 'index.html',
                  {'animals': animals, 'animal_count': animal_count, 'cart_items': cart_items, 'cart': cart,
                   'categories': categories})


def display_about(request):
    return render(request, 'about.html')


def display_contact(request):
    return render(request, 'contact.html')


@login_required
def display_cart(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # Use the related_name 'items' we set in the CartItem model
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart': cart, "user_profile": user_profile})


@login_required
def display_userProfile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'userProfile.html', {'user': user, 'user_profile': user_profile, 'orders': orders})


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


def search_animals(request):
    query = request.GET.get('query', '')
    animals = Animal.objects.filter(common_name__icontains=query)[:5]
    data = [{'id': animal.id, 'name': animal.common_name} for animal in animals]
    return JsonResponse(data, safe=False)


def display_supplies(request):
    categories = SupplyCategory.objects.all()
    supplies = Supplies.objects.all()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    else:
        cart = None
        cart_items = []
    return render(request, 'supplies.html', {'categories': categories, 'supplies': supplies, 'cart_items': cart_items, 'cart': cart})


@login_required
def place_order(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)

        # Create a new order
        order = Order.objects.create(
            user=user,
            complete=True,
            transaction_price=str(cart.total_price)  # Convert Decimal to string
        )

        # Create a string to store order details
        order.save()

        # Clear the cart
        cart.items.all().delete()
        cart.total_price = Decimal('0.00')
        cart.save()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('Store:userProfile')  # Redirect to user profile or order confirmation page

    return redirect('Store:cart')  # Redirect back to cart if not a POST request


@login_required
def add_supply_to_cart(request, supply_id):
    # Get the supply object
    supply = get_object_or_404(Supplies, id=supply_id)

    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the supply is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, supply=supply)

    if not created:
        # If it already exists in the cart, just increase the quantity
        cart_item.quantity += 1
    cart_item.save()

    # Recalculate total price
    cart.total_price = sum(item.total_price for item in cart.items.all())
    cart.save()

    return redirect('Store:supplies')


@login_required(login_url='Store:login')
def add_animal_to_cart(request, animal_id):
    if request.method == "POST":
        # Retrieve the animal instance
        animal = get_object_or_404(Animal, id=animal_id)

        # Extract data from POST request
        quantity = int(request.POST.get('quantity', 1))
        age = int(request.POST.get('age', 1))
        sex = request.POST.get('sex', 'M')

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Try to get or create a CartItem
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            animal=animal,
            age=age,
            sex=sex,
            defaults={'quantity': quantity}
        )

        if not created:
            # If CartItem already exists, update the quantity
            cart_item.quantity += quantity
            cart_item.save()

        # Redirect to the index page or any other page you want
        return redirect('Store:index')

    # If method is not POST, return a 405 Method Not Allowed response
    return HttpResponseNotAllowed(['POST'])


@require_POST
def update_cart_item_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    action = request.POST.get('action')

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return JsonResponse({
        'quantity': item.quantity,
        'total_price': item.total_price,
        'cart_total': item.cart.total_price
    })


@require_POST
def update_cart_item_details(request, item_id):
    item = CartItem.objects.get(id=item_id)
    age = request.POST.get('age')
    sex = request.POST.get('sex')

    if age:
        item.age = int(age)
    if sex:
        item.sex = sex

    item.save()
    return JsonResponse({
        'total_price': item.total_price,
        'cart_total': item.cart.total_price
    })


@require_POST
def remove_cart_item(request, item_id):
    # Get the cart item
    item = get_object_or_404(CartItem, id=item_id)
    cart = item.cart  # Get the associated cart
    item.delete()

    # Recalculate the cart total after removing the item
    cart.recalculate_total()
    cart_total = cart.total_price  # Now get the updated cart total

    return JsonResponse({
        'cart_total': cart_total,
        'item_removed': True,
        'cart_is_empty': cart.items.count() == 0  # Check if cart is empty
    })
