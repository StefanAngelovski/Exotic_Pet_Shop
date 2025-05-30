from django.contrib import admin

from Store.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Animal)
admin.site.register(Supplies)


class OrderItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(UserProfile)
admin.site.register(SupplyCategory)
admin.site.register(Order)
