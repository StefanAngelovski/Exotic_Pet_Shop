from django.urls import path
from Store import views

app_name = 'Store'
urlpatterns = [
    # Pages
    path('', views.display_index, name='index'),
    path('about/', views.display_about, name='about'),
    path('contact/', views.display_contact, name='contact'),
    path('cart/', views.display_cart, name='cart'),
    path('userProfile/', views.display_userProfile, name='userProfile'),
    path('supplies/', views.display_supplies, name='supplies'),

    # User
    path('login/', views.display_login, name='login'),
    path('register/', views.display_register, name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_shipping_details/', views.update_shipping_details, name='update_shipping_details'),

    # Animals
    path('animal/<int:animal_id>/', views.display_animal, name='animal_details'),
    path('search/', views.search_animals, name='search_animals'),

    # Editing Cart
    path('cart/item/update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/item/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),

    # Adding Cart Items
    path('cart/supply/add/<int:supply_id>/', views.add_supply_to_cart, name='add_supply_to_cart'),

    # Placing Order
    path('place_order/', views.place_order, name='place_order'),
]