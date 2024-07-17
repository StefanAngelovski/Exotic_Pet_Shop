from django.urls import path
from Store import views

app_name = 'Store'
urlpatterns = [
    path('', views.display_index, name='index'),
    path('about/', views.display_about, name='about'),
    path('contact/', views.display_contact, name='contact'),
    path('cart/', views.display_cart, name='cart'),
    path('userProfile/', views.display_userProfile, name='userProfile'),
]
