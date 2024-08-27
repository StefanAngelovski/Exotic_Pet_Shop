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
    path('update-cart-item-quantity/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('update-cart-item-details/<int:item_id>/', views.update_cart_item_details, name='update_cart_item_details'),
    path('remove-cart-item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    # Adding Cart Itemss
    path('cart/animal/add/<int:animal_id>/', views.add_animal_to_cart, name='add_animal_to_cart'),
    path('cart/supply/add/<int:supply_id>/', views.add_supply_to_cart, name='add_supply_to_cart'),

    # Placing Order
    path('place_order/', views.place_order, name='place_order'),

]
