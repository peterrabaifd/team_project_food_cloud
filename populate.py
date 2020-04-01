import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_project_food_cloud.settings')

import django
import random
django.setup()
from food_cloud.models import *

def populate():

	meals = {'Test_meal_1': {'description': "Test_meal_1 description", 'price': 15, 'restaurant_slug': "cluckys", 'picture': "static/images/meal_default.jpg", 'average_rating': 4, 'num_orders': 5}, 
			'Test_meal_2': {'description': "Test_meal_2 description", 'price': 15, 'restaurant_slug': "cluckys", 'picture': "static/images/meal_default.jpg", 'average_rating': 4.9, 'num_orders': 10},
			'Test_meal_3': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "cluckys", 'picture': "static/images/meal_default.jpg", 'average_rating': 3.5, 'num_orders': 2}}

	add_restaurant()

	for meal, meal_data in meals.items():
		try:
			c = add_meal(meal, meal_data['description'], meal_data['price'], meal_data['restaurant_slug'], meal_data['average_rating'], meal_data['num_orders'], meal_data['picture'])
		except:
			print("Meal already exists")

def add_restaurant():
	r = RestaurantProfile.objects.get_or_create(user=create_user(), restaurant_name="Clucky's", type="Chicken")
	return r

def create_user():
	try:
		user = User.objects.get(username="TestUser")
	except User.DoesNotExist:
		user = User.objects.create_user(username="TestUser", email=None, password="neverever")

	return user

def add_meal(meal_name, description, price, restaurant_slug, average_rating, num_orders, picture):
	c = Meal.objects.get_or_create(meal_id=random.randrange(1000,10000,1), meal_name=meal_name, description=description, price=price, restaurant_slug=restaurant_slug, picture=picture)[0]
	c.average_rating = average_rating
	c.num_orders = num_orders
	c.save()
	return c
			
# def add_page(cat, title, url, views=0):
	# p = Page.objects.get_or_create(category=cat, title=title)[0]
	# p.url=url
	# p.views=views
	# p.save()
	# return p
	
# def add_cat(name, views=0, likes=0):
	# c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
	# c.save()
	# return c
	
# Start execution here!
if __name__ == '__main__':
	print('Starting population script...')
	populate()