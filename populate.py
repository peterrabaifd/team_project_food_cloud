import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_project_food_cloud.settings')

import django
import random
django.setup()
from food_cloud.models import *
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from food_cloud.models import *
from django.template.defaultfilters import slugify
from django.urls import reverse

def populate():

	meals = {'Bacon Banana Pancakes': {'description': "Bacon banana pancakes", 'price': 15, 'restaurant_slug': "gourmet-dining", 'picture': "/static/images/bacon_banana_pancakes.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Blue Cheese Burger': {'description': "Blue Cheese Burger", 'price': 15, 'restaurant_slug': "burger-emporium", 'picture': "/static/images/blue_cheese_burger.jpg", 'average_rating': 3.5, 'num_orders': 2},
			'Box of Donuts': {'description': "Box of Donuts", 'price': 15, 'restaurant_slug': "cluckys", 'picture': "/static/images/box_of_donuts.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Cabbage Bun Burger': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "burger-emporium", 'picture': "/static/images/cabbage_bun_burger.jpg", 'average_rating': 3.5, 'num_orders': 2},
			'Creamy Tuscan Shrimp Linguine': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "gourmet-dining", 'picture': "/static/images/creamy_tuscan_shrimp_linguine.jpg", 'average_rating': 3.5, 'num_orders': 2},
			'Dinosaur Chicken Nugget Pizza': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "all-day-pizza", 'picture': "/static/images/dinosaur_chicken_nugget_pizza.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Fried Chicken Feet': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "cluckys", 'picture': "/static/images/fried_chicken_feet.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Ham Banana Hollandaise': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "gourmet-dining", 'picture': "/static/images/ham-banana-hollandaise.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Meatball Hotdog': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "hotdogs-galore", 'picture': "/static/images/meatball_hotdog.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Pickle Dog': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "hotdogs-galore", 'picture': "/static/images/pickle_dog.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Standard Burger': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "all-day-pizza", 'picture': "/static/images/standard_burger.jpeg", 'average_rating': 3.5, 'num_orders': 2},
			'Standard Hotdog': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "hotdogs-galore", 'picture': "/static/images/standard_hotdog.jpg", 'average_rating': 3.5, 'num_orders': 2},
			'Trex Burger': {'description': "Test_meal_3 description", 'price': 15, 'restaurant_slug': "burger-emporium", 'picture': "/static/images/trex_burger.jpeg", 'average_rating': 3.5, 'num_orders': 2}}

	add_restaurant()

	for meal, meal_data in meals.items():
		try:
			c = add_meal(meal, meal_data['description'], meal_data['price'], meal_data['restaurant_slug'], meal_data['average_rating'], meal_data['num_orders'], meal_data['picture'])
		except:
			print("Meal already exists")

def add_restaurant():
	r1, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Clucky's"), restaurant_name="Clucky's", type="Chicken")
	r2, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Burger Emporium"), restaurant_name="Burger Emporium", type="Burger")
	r3, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="All day pizza"), restaurant_name="All day pizza", type="Pizza")
	r4, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Gourmet Dining"), restaurant_name="Gourmet Dining", type="Chicken")
	r5, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Hotdogs Galore"), restaurant_name="Hotdogs Galore", type="Hotdog")
	# r1 = RestaurantProfile.objects.get_or_create(user=create_user(), restaurant_name="Clucky's", type="Chicken")
	# r2 = RestaurantProfile.objects.get_or_create(user=create_user(), restaurant_name="Burger Emporium", type="Burger")
	# r3 = RestaurantProfile.objects.get_or_create(user=create_user(), restaurant_name="All day pizza", type="Pizza")
	# r4 = RestaurantProfile.objects.get_or_create(user=create_user(), restaurant_name="Gourmet Dining", type="Chicken")
	# r5 = RestaurantProfile.objects.get_or_create(user=create_user(), restaurant_name="Hotdogs Galore", type="Hotdog")
	#return r

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