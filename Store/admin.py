from django.contrib import admin

from Store.models import *

# Register your models here.
admin.site.register(Category)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(f"Saving animal image: {obj.image}")  # Debug print
        super().save_model(request, obj, form, change)
        print(f"Image after save: {obj.image.url if obj.image else 'No image'}")  # Debug print


@admin.register(Supplies)
class SuppliesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(f"Saving supplies image: {obj.image}")  # Debug print
        super().save_model(request, obj, form, change)
        print(f"Image after save: {obj.image.url if obj.image else 'No image'}")  # Debug print


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
