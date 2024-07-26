from django.urls import path
from Store import views

app_name = 'Store'
urlpatterns = [
    path('', views.display_index, name='index'),
    path('about/', views.display_about, name='about'),
    path('contact/', views.display_contact, name='contact'),
    path('cart/', views.display_cart, name='cart'),
    path('userProfile/', views.display_userProfile, name='userProfile'),
    path('login/', views.display_login, name='login'),
    path('register/', views.display_register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_shipping_details/', views.update_shipping_details, name='update_shipping_details'),
    path('animal/<int:animal_id>/', views.display_animal, name='animal_details'),
    path('add_to_cart/<int:animal_id>/', views.add_to_cart, name='add_to_cart'),
    path('search/', views.search_animals, name='search_animals'),
]