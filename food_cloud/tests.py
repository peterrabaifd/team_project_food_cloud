from django.test import TestCase
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from food_cloud.models import *
from django.template.defaultfilters import slugify
from django.urls import reverse

class meal_and_restaurant_tests(TestCase):
	def setUp(self):
		"""
		Just a setup function for the test restaurant
		"""
		self.r, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username="Clucky's"), restaurant_name="Clucky's", type="Chicken", slug=slugify("Clucky's"))
		print(self.r)
		
	def add_restaurant(restaurant_name, type):
		restaurant, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username=restaurant_name), restaurant_name=restaurant_name, type=type, slug=slugify(restaurant_name))
		restaurant.save()
		return restaurant
		
	def test_ensure_meal_prices_are_positive(self):
		"""
		Checks that meal price is positive
		"""
		meal = Meal(meal_name='Test_meal', description="Test_meal_1 description", price=15, restaurant_slug="cluckys", picture="static/images/meal_default.jpg", average_rating=4, num_orders=5)
		meal.save()
		self.assertEqual((meal.price >= 0), True)
	
	def test_slug_line_creation(self):
		"""
		Checks the test restaurant's slug
		"""
		self.assertEqual(self.r.slug, 'cluckys')
		
class index_view_tests(TestCase):
	def add_restaurant(self, restaurant_name, type):
		restaurant, created = RestaurantProfile.objects.get_or_create(user=User.objects.create_user(username=restaurant_name), restaurant_name=restaurant_name, type=type, slug=slugify(restaurant_name))
		print(restaurant)
		#restaurant.save()
		return restaurant

	def test_index_view_with_no_restaurants(self):
		"""
		If no restaurants exist, the appropriate message should be displayed.
		"""
		response = self.client.get(reverse('food_cloud:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'There are no')
		self.assertQuerysetEqual(response.context['restaurants'], [])
		
	def test_index_view_with_restaurants(self):
		"""
		Checks whether restaurants are displayed correctly when present.
		"""
		rest1 = self.add_restaurant('Test_restaurant1', 'chicken')
		rest2 = self.add_restaurant('Test_restaurant2', 'chicken')
		rest3 = self.add_restaurant('Test_restaurant3', 'chicken')
		response = self.client.get(reverse('food_cloud:index'))
		print("Debug printing response", response.context['restaurants'])
		self.assertEqual(response.status_code, 200)
		self.assertEqual(rest1 in RestaurantProfile.objects.all(), True)
		self.assertEqual(rest2 in RestaurantProfile.objects.all(), True)
		self.assertEqual(rest3 in RestaurantProfile.objects.all(), True)
		num_categories = len(response.context['restaurants'])
		self.assertEquals(num_categories, 3)