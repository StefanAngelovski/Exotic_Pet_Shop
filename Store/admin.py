from django.contrib import admin

from Store.models import *

# Register your models here.
admin.site.register(Animal)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(UserProfile)

