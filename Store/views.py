from django.shortcuts import render

from Store.models import Category


# Create your views here.
def display_index(request):
    return render(request, 'index.html', {'categories': Category.objects.all()})
