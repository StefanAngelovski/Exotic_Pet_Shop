from django.shortcuts import render

from Store.models import Category


# Create your views here.
def display_index(request):
    return render(request, 'index.html', {'categories': Category.objects.all()})


def display_about(request):
    return render(request, 'about.html')


def display_contact(request):
    return render(request, 'contact.html')


def display_cart(request):
    return render(request, 'cart.html')


def display_userProfile(request):
    return render(request, 'userProfile.html')

