from django.contrib import admin
from food_cloud.models import *

class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('restaurant_name',)
	prepopulated_fields = {'slug':('restaurant_name',)}

class MealAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('meal_name',)}
	list_display = ('meal_name', 'restaurant_slug', 'num_orders')

class RatingAdmin(admin.ModelAdmin):
	list_display = ('meal', 'rating')

class UserAdmin(admin.ModelAdmin):
	list_display = ('user',)

admin.site.register(UserProfile, UserAdmin)
admin.site.register(RestaurantProfile, RestaurantAdmin)
admin.site.register(Meal, MealAdmin)