from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from io import open_code

from multiselectfield import MultiSelectField

ALLERGENS = (
                (1, 'Cereals containing gluten'),
                (2, 'Crustaceans'),
                (3, "Eggs"),
                (4, "Fish"),
                (5, "Peanuts"), 
                (6, " Soybeans"), 
                (7, "Milk (Lactose)"), 
                (8, "Nuts"), 
                (9, "Celery"), 
                (10, "Mustard"), 
                (11, "Sesame seeds"), 
                (12, "Sulphur dioxide and sulphites"), 
                (13, "Lupin"), 
                (14, "Molluscs"),
                (15, "Pork"),
                (16, "Beef")
                )


class Account(models.Model): # User profile use with google authentication, use access token to get info and then create user with api

    acc = models.OneToOneField(User, on_delete=models.CASCADE,  blank=True, null=True)
    is_reg = models.BooleanField(default=False)
    image = models.ImageField(upload_to='user_images', null=True)
    sex = models.TextField(null=True,  max_length=1) #null = not defined, F = Female, M = Male
    age =  models.IntegerField(default=0, null=True) # has to be 17 - 100 
    weight =  models.DecimalField(max_digits= 5, decimal_places=2, default=0.0, null=True) # weight cant be a mad number
    height =  models.IntegerField(default=0, null=True) # give options for inches, cm, but eveyrthing is translated to cm to make it easier 
    activity_level = models.DecimalField(max_digits= 5, decimal_places=3, default=0.0, null=True) # translate to numbers 0 - not active etc
    date = models.DateField(null=True)
    dietary_req =  MultiSelectField(choices=ALLERGENS, max_length=100, null=True, blank=True) # string with all ditery requirements/allergens ('ADMHUHG')
    preferences =  models.TextField(null=True) # foods that they like link to id numbers
    main_calories = models.IntegerField(default=0, null=True) #Maintenance calories
    remain_calories = models.IntegerField(default=0, null=True) # reset each day
    remain_protein = models.IntegerField(default=0, null=True) # reset each day
    remain_fats = models.IntegerField(default=0, null=True) # reset each day
    remain_carbs = models.IntegerField(default=0, null=True) # reset each day

    # this needs to be calcauled after rest of info is given
    protein = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
    fats = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
    carbs = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams

class Menu(models.Model): # Each menu contains specific meals
    id =  models.IntegerField(primary_key=True)
    name = models.TextField() #Cafeteria, Nubar Etc
    is_active = models.BooleanField(default=True) # admin might have taken down menu

    def __str__(self):
       return self.name

class Meal(models.Model): # Specific meals, belong to menus
    id =  models.IntegerField(primary_key=True) 
    image = models.ImageField(upload_to='meals', null=True)
    manu_id =  models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True)
    name = models.TextField(blank=True) 
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits= 6, decimal_places=2, default=0.0)
    calories = models.IntegerField(default=0) 
    allergens =  MultiSelectField(choices=ALLERGENS, max_length=100, null=True, blank=True)
    protein = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
    fats = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
    carbs = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
    special = models.BooleanField(default=False)
    rating = models.IntegerField(default=0) # out of 5 stars
    user_rank = models.IntegerField(default=0)
    ordered = models.IntegerField(null=True, default=0, blank = True)  # food was eaten and ordered
    munched = models.IntegerField(null=True, default=0)  # user might have just bought some food but not through the app and still wants to track calories
    is_active = models.BooleanField(default=True) # see if admin wanted to hide it maybe not available 
    liked = models.ManyToManyField(User, default=None, blank = True)

    def __str__(self):
       return self.name
     
    @property
    def num_likes(self):
        return self.liked.all().count()


class Recipe(models.Model): # Recipes contain singualar recipe
     id =  models.IntegerField(primary_key=True) 
     image = models.ImageField(upload_to='recipes', null=True)
     name = models.TextField() 
     author = models.TextField() 
     ingredients = models.TextField()
     serving_size = models.IntegerField(default=0) 
     prep_time = models.IntegerField(default=0) 
     cook_time = models.IntegerField(default=0) 
     desc = models.TextField() 
     method = models.TextField()
     notes = models.TextField(null=True)
     calories = models.IntegerField(default=0) 
     allergens =  MultiSelectField(choices=ALLERGENS, max_length=100, null=True, blank=True)
     protein = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
     fats = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
     carbs = models.DecimalField(max_digits= 5, decimal_places=2, default=0.0) #grams
     rating = models.IntegerField(default=0) # out of 5 stars
     user_rank = models.IntegerField(default=0)
     munched = models.IntegerField(null=True, default=0, blank = True)  # user might have just bought some food but not through the app and still wants to track calories
     is_active = models.BooleanField(default=True) # see if admin wanted to hide it 
     liked = models.ManyToManyField(User, default=None, blank = True)

     def __str__(self):
       return self.name

     @property
     def num_likes(self):
         return self.liked.all().count()
    

CHOICES = (
    ('like', 'like'),
     ('Unlike', 'Unlike'),
)

class LikeRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id =  models.ForeignKey( Recipe, on_delete=models.CASCADE)
    value = models.CharField(choices=CHOICES, default='Like', max_length=10 )
  
    def __str__(self):
       return self.post_id.name

class LikeMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id =  models.ForeignKey(Meal, on_delete=models.CASCADE)
    value = models.CharField(choices=CHOICES, default='Like', max_length=10 )
  
    def __str__(self):
       return self.post_id.name

class Basket(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class BasketItem(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def product_name(self):
        return self.product_id.name
    
    def price(self):
        return self.product_id.price * self.quantity

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits= 6, decimal_places=2, default=0.0)
    name = models.TextField()
    studentId = models.CharField(max_length=8)
    email = models.EmailField(max_length = 254)

class MunchBasket(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class MunchBasketItem(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(MunchBasket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def product_name(self):
        return self.product_id.name
    
    def cals(self):
        return self.product_id.calories * self.quantity