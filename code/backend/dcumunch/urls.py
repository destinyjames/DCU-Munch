
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'meals', views.MealViewSet)
router.register(r'recipe', views.RecipeViewSet)
router.register(r'menus', views.MenuViewSet)
router.register(r'baskets', views.BasketViewSet)
router.register(r'munchbasket', views.MunchBasketViewSet)
router.register(r'likemeals', views.LikeMealViewSet)
router.register(r'likerecipe', views.LikeRecipeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'orders', views.OrderViewSet)




urlpatterns = [
    path('', views.index, name="home"),
    path('', include(router.urls)),
    path('all-meals/<int:prodid>', views.meal_individual, name="individual_meal"),
    path('all-recipes/<int:prodid>', views.recipe_individual, name="individual_recipe"),
    path('', TemplateView.as_view(template_name="feed.html")),
    path('accounts/', include('allauth.urls')),
    path('login/', views.login, name="login"),
    path('all-meals/', views.allmeals, name="allmeals"),
    path('all-recipes/', views.allrecipes, name="allrecipes"),
    path('removeitem/<int:sbi>', views.remove_item, name="remove_item"),
    path('register/', views.register, name="register"),
    path('admin/quickadd/', views.quickadd, name="register"),
    path('foodsearch/', views.food_search, name="foodsearch"),
    path('like/<int:meal_id>', views.like_postmeal, name="like-postmeal"),
    path('stats/', views.stats, name="stats"),
    path('newmeal/<str:newmealname>', views.newmeal, name="newmeal"),
    path('addmeal/<str:newmealname>', views.addmeal, name="addmeal"),
    path('logout/', views.logout_view, name='logout'),
    path('likerecipe/<int:recipe_id>', views.like_recipe, name="like-recipemeal"),
    path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
    path('order/', views.order, name='order'),
    path('userprofile/', views.userprofile, name="basket"),
    path('orderhistory/', views.previous_orders, name="order_history"),
    path('currentorders/', views.current_orders, name="current_orders"),
    path('doneorder/<int:orderid>', views.done_order, name="done_orders"),
    path('basket/', views.show_basket, name="basket"),
    path('munch/<int:mealid>', views.muncher, name="muncher"),
    path('munchdiary/', views.munchshow_basket, name="munchbasket"),
    path('munchremoveitem/<int:sbi>', views.munchremove_item, name="remove_item"),
  
    
]