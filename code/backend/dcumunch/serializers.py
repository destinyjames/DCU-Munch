from rest_framework import serializers
from .models import *


class AccountSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Account
        fields = ['is_reg', 'image', 'sex', 'age', 'weight', 'height', 'activity_level', 'date', 'dietary_req',  'main_calories',
                  'remain_calories', 'remain_protein', 'remain_fats', 'remain_carbs', 'protein', 'fats', 'carbs' ]   

class UserSerializer(serializers.HyperlinkedModelSerializer):
    extrainfo = AccountSerializer(many=False, read_only=True, source='account')
    user_permissions = serializers.StringRelatedField(many=True)
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', "url", 'password', "last_login", "is_superuser", "username", "first_name", "last_name", "email",  "is_staff",  "is_active", "date_joined", "groups",  
                    "user_permissions",  'extrainfo' ]
  

class MealSerializer(serializers.HyperlinkedModelSerializer):
    manu_id = serializers.StringRelatedField(many=False)
    liked = serializers.StringRelatedField(many=True, read_only=True)
    allergens = serializers.CharField()

    class Meta:
        model = Meal
        fields = ['id', 'image', 'name', 'desc', 'price', 'calories', 'allergens', 'protein', 'fats', 'carbs',
                  'special', 'rating', 'user_rank', 'ordered', 'munched', 'is_active', 'manu_id', 'liked' ]

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    liked = serializers.StringRelatedField(many=True, read_only=True)
    allergens = serializers.CharField()
    
    class Meta:
        model = Recipe
        fields = ['id', "url", 'image', 'name', 'author', 'ingredients', 'serving_size', 'prep_time', 'cook_time', 'desc', 'method', 'notes', 'calories', 'allergens', 'protein', 'fats', 'carbs',
                   'rating', 'user_rank', 'munched','is_active', 'liked' ]

class LikeMealSerializer(serializers.ModelSerializer):
    post_id = MealSerializer(many=False, read_only=True)
    user = serializers.HyperlinkedRelatedField(
        many= False,
        read_only=True,
        view_name='user-detail'
    )

    post_id = serializers.HyperlinkedRelatedField(
        many= False,
        read_only=True,
        view_name='meal-detail'
    ) 
    
    class Meta:
        model = LikeMeal
        fields = ['user', 'post_id', 'value' ]


class LikeRecipeSerializer(serializers.HyperlinkedModelSerializer):
    post_id = MealSerializer(many=False, read_only=True)
    user = serializers.HyperlinkedRelatedField(
        many= False,
        read_only=True,
        view_name='user-detail'
    )

    post_id = serializers.HyperlinkedRelatedField(
        many= False,
        read_only=True,
        view_name='recipe-detail'
    ) 
    
    class Meta:
        model = LikeRecipe
        fields = ['user', 'post_id', 'value' ]


class MenuSerializer(serializers.ModelSerializer):
    items = MealSerializer(many=True, read_only=True, source='meal_set')
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'is_active', 'items']


class BasketItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['product_id', 'product_name', 'quantity', 'price']

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemsSerializer(many=True, read_only=True, source='basketitem_set')

    class Meta:
        model = Basket
        fields = ['id', 'user_id', 'is_active', 'items']

class AddBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['product_id']
    
    def create(self, validated_data):
        product_id = validated_data['product_id']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(user_id=current_user, is_active=True).first()
            # Check if the item is already in the basket
            basket_items = BasketItem.objects.filter(product_id=product_id, basket_id=shopping_basket).first()
            if basket_items:
                basket_items.quantity = basket_items.quantity + 1 # if it is already in the basket, add to the quantity
                basket_items.save()
                return basket_items
            else:
                new_basket_item = BasketItem.objects.create(basket_id = shopping_basket, product_id=product_id)
                return new_basket_item
            
        else:
            return None

class RemoveBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['product_id']


    def create(self, validated_data):
        product_id = validated_data['product_id']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(user_id=current_user, is_active=True).first()
            # Check if the item is already in the basket
            basket_items = BasketItem.objects.filter(product_id=product_id, basket_id=shopping_basket).first()
            if basket_items:
                if basket_items.quantity > 1:
                    basket_items.quantity = basket_items.quantity - 1 # if it is already in the basket, add to the quantity
                    basket_items.save()
                    return basket_items
                else:
                    basket_items.delete()
                    return BasketItem(basket_id=shopping_basket, product_id=product_id, quantity=0)
            else:
                return BasketItem(basket_id=shopping_basket, product_id=product_id, quantity=0)
        else:
            return None

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'basket_id', 'date_ordered', 'user_id']


class MunchBasketItemsSerializer(serializers.ModelSerializer):

    product_id = serializers.HyperlinkedRelatedField(
        many= False,
        read_only=True,
        view_name='recipe-detail'
    ) 
    
    
    class Meta:
        model = MunchBasketItem
        fields = ['product_id', 'product_name', 'quantity']



class MunchBasketSerializer(serializers.ModelSerializer):
    items = MunchBasketItemsSerializer(many=True, read_only=True, source='munchbasketitem_set')
     
    user_id = serializers.HyperlinkedRelatedField(
        many= False,
        read_only=True,
        view_name='user-detail'
    )
    class Meta:
        model = MunchBasket
        fields = ['id', 'user_id', 'is_active', 'items']



