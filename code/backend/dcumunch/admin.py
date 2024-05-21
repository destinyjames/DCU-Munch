from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, User
from .models import *


admin.site.index_template = "newindex.html"

admin.site.register(Menu)
admin.site.register(Meal)
admin.site.register(Recipe)
admin.site.register(LikeRecipe)
admin.site.register(LikeMeal)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)
admin.site.register(MunchBasket)
admin.site.register(MunchBasketItem)


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'
    
class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)


