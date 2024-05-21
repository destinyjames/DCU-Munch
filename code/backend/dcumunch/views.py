from inspect import getmembers
from pickle import NONE
import re
import tempfile
from rest_framework import generics
import requests as rq
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
import random
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from py_edamam import Edamam
import json
import random
from qrcode import *
from django.contrib.auth import logout
import os
import glob
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

# Feed algorthim based on Facebook Edge rank
# List highest infiity score

def munch_alogrithim(request, objects):
    nominees = []
    for m in objects:
        if  str(m.allergens) != 'None' and str(request.user.account.dietary_req) != '' :
            userallergens = set(str((request.user.account.dietary_req)).split(","))
            meal_allergens = set(str((m.allergens)).split(","))
            allergns_same = userallergens.intersection(meal_allergens)
            if (allergns_same) :
                pass
            elif m.protein > request.user.account.protein or m.fats > request.user.account.fats or m.carbs > request.user.account.carbs or m.calories > request.user.account.remain_calories: 
                #print(m)
                pass
            else:
                #print(m)
                nominees.append(m)
        else:
            if m.protein > request.user.account.protein or m.fats > request.user.account.fats or m.carbs > request.user.account.carbs or m.calories > request.user.account.remain_calories: 
                #print(m)
                pass
            else:
                #print('Here')
                nominees.append(m)

    def ratingret(elem):
        return elem.user_rank

    for n in nominees: #trying to give 3 sqaure meals a day
        n.user_rank = n.rating
        if n.calories <= (float(request.user.account.remain_calories) * 0.33) :
            n.user_rank += 2
        if n.protein <= (float(request.user.account.remain_protein)* 0.33): 
            n.user_rank += 1
        if n.carbs <= (float(request.user.account.remain_carbs) * 0.33):
            n.user_rank += 1
        if n.fats <= (float(request.user.account.remain_fats) * 0.33):
            n.user_rank += 1 
        n.save()

    

    nominees.sort(key=ratingret, reverse=True) # sort on users rating 
    return nominees

def save_image_from_url(model, url):
    r = rq.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.image.save("image.jpg", File(img_temp), save=True)

@login_required(login_url='/login/')
def index(request):

    today = date.today()
    if str(request.user.account.date) != str(today):
      
       request.user.account.remain_calories = request.user.account.main_calories
       request.user.account.remain_protein =  request.user.account.protein
       request.user.account.remain_fats =  request.user.account.fats
       request.user.account.remain_carbs =  request.user.account.carbs
       request.user.account.date = today
       request.user.account.save()
       request.user.save()

    Munchbasket = MunchBasket.objects.filter(user_id=request.user, is_active=True).first()
    if Munchbasket is None:
       request.user.account.remain_calories = request.user.account.main_calories
       request.user.account.remain_protein =  request.user.account.protein
       request.user.account.remain_fats =  request.user.account.fats
       request.user.account.remain_carbs =  request.user.account.carbs
       request.user.account.date = today
       request.user.account.save()
       request.user.save()


    meals = Meal.objects.all()
    recipes = Recipe.objects.all()

    nominees = munch_alogrithim(request, meals)
    nominees_2 = munch_alogrithim(request, recipes)
    
    if len(nominees) == 0: 
        meal = None
    else: 
        meal = random.choice(nominees)

    if len(nominees_2) == 0: 
        recipe_1 = None
    else: 
        recipe_1 = random.choice(nominees_2)
    
    mealdeals = [m for m in nominees if m.special == True]

    if len(mealdeals) == 0: 
         meal_2 = None
    else: 
         meal_2 = random.choice(mealdeals)

    #print(meal, recipe_1, meal_2)
    return render(request, 'feed.html', {'recommended':meal, 'deal':meal_2, 'recipe':recipe_1})
    
def meal_individual(request, prodid):
    meal = Meal.objects.get(id=prodid)
    return render(request, 'individualmeal.html',{'product': meal} )

def recipe_individual(request, prodid):
    recipe = Recipe.objects.get(id=prodid)
    return render(request, 'individualrecipe.html',{'product': recipe} )

def login(request):
    return render(request, 'login.html')


def register(request):
    target = None
    print(request.method)
    if ((hasattr(request.user, 'account')) & (request.method != 'POST')):
        return HttpResponseRedirect("/")
    elif request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                
                g_accounts = (SocialAccount.objects.all())
                for accounts in g_accounts:
                    if str(accounts) == str(request.user):
                         target = accounts
                         
                request.user.account.image = target.extra_data['picture']
                request.user.account.sex = request.POST.get('sex')
                request.user.account.age = int(request.POST.get('age'))
                request.user.account.weight = int(float(request.POST.get('weight')))
                request.user.account.height = (request.POST.get('height'))
                request.user.account.activity_level = float(request.POST.get('activity_level'))
                request.user.account.dietary_req = request.POST.get('dietary_req')
                request.user.account.preferences = request.POST.get('preferences')
                request.user.account.date = date.today()
                request.user.account.save()
                request.user.save()

                calc_macros(request.user)
              
                return HttpResponseRedirect("/")
    else:
        form = UserForm()
        Account.objects.filter(acc=request.user).delete()
        Account.objects.create(acc=request.user)
        request.user.account.is_reg = True
        request.user.account.save()
       
        submitted = False

    #form.save()
    return render(request, 'register_user.html', {'form':form})

# (https://code-projects.org/calorie-calculator-in-javascript-with-source-code/)
# https://www.acsm.org/docs/default-source/files-for-resource-library/protein-intake-for-optimal-muscle-maintenance.pdf
# https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/carbohydrates/art-20045705#:~:text=How%20many%20carbohydrates%20do%20you,grams%20of%20carbs%20a%20day.
# https://youtu.be/OWxvX4m_h7c -Endaman API

def calc_macros(user):
    if user.account.sex == "M":
        user.account.main_calories = int(user.account.activity_level * (66.5 + (13.75 * int((user.account.weight))) + (5.003 * int(user.account.height)) - (6.755 * int(user.account.age))))
        user.account.protein = int((.4 * user.account.main_calories) / 4)
        user.account.carbs = int((.4 * user.account.main_calories) / 4)
        user.account.fats = int((.2 * user.account.main_calories) / 9)
        user.account.remain_calories =  user.account.main_calories 
        user.account.save()
        user.save()
    else:
        user.account.main_calories = int(user.account.activity_level * (655 + (9.563 * (user.account.weight))) + (1.850 * user.account.height) - (4.676 * user.account.age))
        user.account.protein = int((.4 * user.account.main_calories) / 4)
        user.account.carbs = int((.4 * user.account.main_calories) / 4)
        user.account.fats = int((.2 * user.account.main_calories) / 9)
        user.account.remain_calories =  user.account.main_calories 
        user.account.save()
        user.save()


"""@login_required ---- use youtube video for like button
def like(request, mealid):
     munched_meal = Meal.objects.get(id=mealid)
     munchel_meal """
     

@login_required
def allmeals(request):
    meals = Meal.objects.all()
    return render(request, 'all_meals.html', {"meals" : meals})

def allrecipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'all_recipes.html', {"recipes" : recipes})

@csrf_exempt
def like_postmeal(request, meal_id):
    user = request.user
    if request.method == 'POST':

        meal = Meal.objects.get(id=meal_id)

        if user in meal.liked.all():
            meal.liked.remove(user)
        else:
            meal.liked.add(user)
        
        like, created = LikeMeal.objects.get_or_create(user=user, post_id=meal)

        if not created:
            if like.value == "Like":
                like.value = 'Unlike'
            else: 
                like.value == "Like"

        meal.rating = meal.liked.all().count()
        meal.save()
        like.save()
    return redirect('/')

@csrf_exempt
def like_recipe(request, recipe_id):
    user = request.user
    if request.method == 'POST':

        recipe = Recipe.objects.get(id=recipe_id)

        if user in recipe.liked.all():
            recipe.liked.remove(user)
        else:
            recipe.liked.add(user)
        
        like, created = LikeRecipe.objects.get_or_create(user=user, post_id=recipe)

        if not created:
            if like.value == "Like":
                like.value = 'Unlike'
            else: 
                like.value == "Like"
        recipe.rating = recipe.liked.all().count()
        recipe.save()
        like.save()
    return redirect('/')

def quickadd(request, hits):
    return render(request, 'quickadd.html', hits)

# user must put in allergies 
@csrf_exempt
def food_search(request):
      if not(request.user.is_superuser):
          return redirect("/")
      if request.method == 'POST':
          app_id  =  'ae3e4902'
          app_key = '456fd73958e0fdc2c3063a8d116ba94e'
          ingr =  request.POST.get("searchobj")
          url = f'https://api.edamam.com/api/food-database/v2/parser?ingr={ingr}&app_id={app_id}&app_key={app_key}'
          response = rq.get(url)
          hits = response.json()
          #print(ingredients["hints"][0]['food']['label'])
          food = hits["hints"]
          #print(hits)
          return quickadd(request, hits)

   
      return render(request, 'food_search.html')

@csrf_exempt
def newmeal(request, newmealname):
        if not(request.user.is_superuser):
          return redirect("/")
        num, name = newmealname.split('+')
        app_id  =  'ae3e4902'
        app_key = '456fd73958e0fdc2c3063a8d116ba94e'
        url = f'https://api.edamam.com/api/food-database/v2/parser?ingr={name}&app_id={app_id}&app_key={app_key}'
        response = rq.get(url)
        hits = response.json()
        #print(ingredients["hints"][0]['food']['label'])
        food = hits["hints"]
        i = 0 
        while i < len(food):
            if (food[i]['food']['foodId']) == num:
                    target = food[i]['food']
                   # print("FOUND")
                    #print(target)
                    
                    return render(request, 'addthismeal.html', target )
            i = i + 1 
@csrf_exempt
def addmeal(request, newmealname):
        if not(request.user.is_superuser):
          return redirect("/")
        num, name, menu = newmealname.split('+')
        app_id  =  'ae3e4902'
        app_key = '456fd73958e0fdc2c3063a8d116ba94e'
        url = f'https://api.edamam.com/api/food-database/v2/parser?ingr={name}&app_id={app_id}&app_key={app_key}'
        response = rq.get(url)
        hits = response.json()
        #print(ingredients["hints"][0]['food']['label'])
        food = hits["hints"]
        i = 0 
        while i < len(food):
            if (food[i]['food']['foodId']) == num:
                    target = food[i]['food']
                    break
            i = i + 1 

        print("FOUND")
        #print(target)
         
        menu = Menu.objects.get(id=int(menu))
        print(target['nutrients'])


        
        b = Meal(id = random.randint(1, 1000000), name = target['label'],  manu_id = menu, protein=target['nutrients']['PROCNT'], calories=target['nutrients']['ENERC_KCAL'], fats=target['nutrients']['FAT'], carbs=target['nutrients']['CHOCDF'])

        if 'image' in target:
            save_image_from_url(b, target['image'])
            b.save()
        else:
            image_url = "favicon_munch.png"
            b.image = image_url
            b.save()


        new_meal_url =  "/admin/dcumunch/meal/" + str(b.id) + "/change/"
        return redirect(new_meal_url)

def liked(elem):
        
        return elem.user_rank

def munched(elem):
        return elem.munched

def ordered(elem):
        return elem.ordered

def stats(request):

    if not(request.user.is_superuser):
       print("hejhjehjfhjhf")
       return redirect("/")

    meal_objs = Meal.objects.all()
    recipe_objs = Recipe.objects.all()
    
    meals = []
    for m in meal_objs:
        meals.append(m)

    recipes = []
    for r in recipe_objs:
        recipes.append(r)


    meals.sort(key=liked)
    mostliked_meals = meals[:]
    meals.sort(key=munched, reverse=True)
    mostmunched_meals = meals[:]
    meals.sort(key=ordered, reverse=True)
    mostorderd_meals = meals[:]

    print(mostliked_meals)
    print(recipes)
    
    recipes.sort(key=liked, reverse=True)
    mostliked_recipe  = recipes[:]
    #recipes.sort(key=munched, reverse=True)
    mostmunched_recipe = recipes[:]

    
    return render(request, 'admin_stats.html', 
    {"toplikedmeals" :  mostliked_meals, "topmunchedmeals" :  mostmunched_meals, "toporderedmeals" :   mostorderd_meals, "toplikedrecipes": mostliked_recipe, "topmunchedrecipes": mostmunched_recipe})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect("/")

def add_to_basket(request, prodid):
    user = request.user
    # is there a shopping basket for the user 
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        # create a new one
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # get the product 
    product = Meal.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        # there is no basket item for that product 
        # create one 
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        # a basket item already exists 
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return render(request, 'individualmeal.html', {'product': product, 'added':True})

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return render(request, 'basket.html', {'empty':True})
        
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        if sbi.exists():
            return render(request, 'basket.html',{'basket':basket, 'sbi':sbi})
            
        else:
             return render(request, 'basket.html', {'empty':True})

@login_required
def remove_item(request,sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket")
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity - 1
            basketitem.save()
        else:
            basketitem.delete()
    return redirect("/basket")
        

@login_required
def order(request):
    # load in all data we need, user, basket, items
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect("/")
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists(): # if there are no items
        return redirect("/")
    # POST or GET
    if request.method == "POST":
        # check if valid
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.id = random.randint(1, 1000000)
            order.user_id = user
            order.basket_id = basket
            total = 0.0
            locations = []
            for item in sbi:
                meal = item.product_id
                meal.ordered = meal.ordered + 1
                total += float(item.price())
                places = meal.manu_id
                if places not in locations:
                    locations.append(places.name)

            locations = ','.join(locations)
            data = str(order.name) + "-"  + str(order.studentId) + "-" + str(order.id)
            img=make(data)
            img.save("media/" + "qrcodes/" + str(order.id) + ".png" )
            order.total_price = total
            order.save()
            basket.save()
            return render(request, 'ordercomplete.html', {'order':order, 'basket':basket, 'sbi':sbi, 'locations':locations})
        else:
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})
    else:
        # show the form
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders':orders})

@login_required
def userprofile(request):
    return render(request, 'userprofile.html')

@login_required
def current_orders(request):
    ls = []
    basket = []

    if not(request.user.is_superuser) and not(request.user.is_staff):
        return redirect("/")
       
    orders = Order.objects.all()
    for order in orders:
        basket  = order.basket_id
        if basket.is_active:
            preplist = BasketItem.objects.filter(basket_id=basket)
            a = preplist
            ls.append(a) 
            print(ls)
    return render(request, 'currentorders.html', {'orders':ls, 'orderid':basket})


def done_order(request, orderid):
    if not(request.user.is_superuser):
       return redirect("/")

    basket = Basket.objects.get(id=orderid)
    basket.is_active = False
    basket.save()

    name = Order.objects.get(basket_id=orderid)
    os.remove("media/" + "qrcodes/" + str(name.id) + ".png")
    return redirect("/currentorders")
                   

def muncher(request, mealid):
    user = request.user
    # is there a shopping basket for the user 
    basket = MunchBasket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        # create a new one
        MunchBasket.objects.create(user_id = user)
        basket = MunchBasket.objects.filter(user_id=user, is_active=True).first()
    # get the product )
    
    try:
       product = Meal.objects.get(id=mealid)
    except:
       product = Recipe.objects.get(id=mealid)

    if not (product.munched):
         product.munched = 1
         product.save()
         user.account.remain_calories = user.account.remain_calories - product.calories
         user.account.remain_protein =  request.user.account.remain_protein - product.protein
         user.account.remain_fats =  request.user.account.remain_fats - product.fats
         user.account.remain_carbs =  request.user.account.remain_carbs - product.carbs
         user.account.save()
         user.save()
    else:
        product.munched = product.munched + 1
        product.save()
        user.account.remain_calories = user.account.remain_calories - product.calories
        user.account.remain_protein =  request.user.account.remain_protein - product.protein
        user.account.remain_fats =  request.user.account.remain_fats - product.fats
        user.account.remain_carbs =  request.user.account.remain_carbs - product.carbs
        user.account.save()
        user.save()

    sbi = MunchBasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        # there is no basket item for that product 
        # create one 
        sbi = MunchBasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        # a basket item already exists 
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return  redirect('/munchdiary')

@login_required
def munchshow_basket(request):
    user = request.user
    basket = MunchBasket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
          request.user.account.remain_calories = request.user.account.main_calories
          request.user.account.remain_protein =  request.user.account.protein
          request.user.account.remain_fats =  request.user.account.fats
          request.user.account.remain_carbs =  request.user.account.carbs
          user.account.save()
          user.save()
          return render(request, 'Munchbasket.html', {'empty':True})   
    else:
        sbi = MunchBasketItem.objects.filter(basket_id=basket)
        if sbi.exists():
            return render(request, 'Munchbasket.html',{'basket':basket, 'sbi':sbi})
            
        else:
              request.user.account.remain_calories = int(request.user.account.main_calories)
              request.user.account.remain_protein =  int(request.user.account.protein)
              request.user.account.remain_fats =  int(request.user.account.fats)
              request.user.account.remain_carbs =  int(request.user.account.carbs)
              user.account.save()
              user.save()
              basket.delete()
              return render(request, 'Munchbasket.html', {'empty':True})

@login_required
def munchremove_item(request,sbi):
    user = request.user
    basketitem = MunchBasketItem.objects.get(id=sbi)
    if basketitem is None:

        return redirect("/munchdiary")
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity - 1
            user.account.remain_calories = user.account.remain_calories + basketitem.product_id.calories
            user.account.remain_protein =  request.user.account.remain_protein + basketitem.product_id.protein
            user.account.remain_fats =  request.user.account.remain_fats + basketitem.product_id.fats
            user.account.remain_carbs =  request.user.account.remain_carbs + basketitem.product_id.carbs
            user.account.save()
            user.save()
            basketitem.save()
        else:
            user.account.remain_calories = user.account.remain_calories + basketitem.product_id.calories
            user.account.remain_protein =  request.user.account.remain_protein + basketitem.product_id.protein
            user.account.remain_fats =  request.user.account.remain_fats + basketitem.product_id.fats
            user.account.remain_carbs =  request.user.account.remain_carbs + basketitem.product_id.carbs
            user.account.save()
            user.save()
            basketitem.delete()
          

    return redirect("/munchdiary")


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BasketViewSet(viewsets.ModelViewSet):
  serializer_class = BasketSerializer
  queryset = Basket.objects.all()
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
      user = self.request.user # get the current user
      if user.is_superuser:
          return Basket.objects.all() # return all the baskets if a superuser requests
      else:
          # For normal users, only return the current active basket
          shopping_basket = Basket.objects.filter(user_id=user, is_active=True)
          return shopping_basket


class LikeMealViewSet(viewsets.ModelViewSet):
    serializer_class = LikeMealSerializer
    queryset = LikeMeal.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user # get the current user
        if user.is_superuser:
            return LikeMeal.objects.all() # return all the baskets if a superuser requests
        else:
            # For normal users, only return the current active basket
            meals = LikeMeal.objects.filter(user_id=user)
            return meals


class LikeRecipeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeRecipeSerializer
    queryset = LikeRecipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user # get the current user
        if user.is_superuser:
            return LikeRecipe.objects.all() # return all the baskets if a superuser requests
        else:
            # For normal users, only return the current active basket
            recipes = LikeRecipe.objects.filter(user_id=user)
            return recipes

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user # get the current user
        if user.is_superuser:
            return Order.objects.all() # return all the baskets if a superuser requests
        else:
            # For normal users, only return the current active basket
            orders = Order.objects.filter(user_id=user)
            return orders

class MunchBasketViewSet(viewsets.ModelViewSet):
  serializer_class = MunchBasketSerializer
  queryset = MunchBasket.objects.all()
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
      user = self.request.user # get the current user
      if user.is_superuser:
          return MunchBasket.objects.all() # return all the baskets if a superuser requests
      else:
          # For normal users, only return the current active basket
          shopping_basket = MunchBasket.objects.filter(user_id=user, is_active=True)
          return shopping_basket


