from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from food_cloud.models import *
from food_cloud.forms import *
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from food_cloud.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from food_cloud.bing_search import run_query
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify


def index(request):
	context_dict = get_context_dict(request)
	context_dict['restaurants'] = RestaurantProfile.objects.order_by(
		'average_rating')[:5]
	context_dict['meals'] = Meal.objects.order_by(
		'-num_orders', '-average_rating')[:5]

	response = render(request, 'food_cloud/index.html', context=context_dict)
	return response


def index_restaurant(request):
	context_dict = {}

	meal_list = Meal.objects.order_by('meal_name')

	context_dict = {}
	context_dict['meals'] = meal_list

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(
		request, 'food_cloud/index_restaurant.html', context=context_dict)
	return response


def register_choice(request):
	context_dict = {}
	response = render(
		request, 'food_cloud/register_choice.html', context=context_dict)
	return response


def login_choice(request):
	context_dict = {}
	response = render(request, 'food_cloud/login_choice.html',
					  context=context_dict)
	return response


def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			registered = True
			user_login(request)
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'food_cloud/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def register_restaurant(request):
	registered = False

	if request.method == 'POST':
		user_form = RestaurantForm(request.POST)
		profile_form = RestaurantProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = True
			user_login(request)
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = RestaurantForm()
		profile_form = RestaurantProfileForm()
	return render(request, 'food_cloud/register_restaurant.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				try:
					customer = UserProfile.objects.get(user=user)
				except UserProfile.DoesNotExist:
					return redirect(reverse('food_cloud:login_restaurant'))
				login(request, user)
				return redirect(reverse('food_cloud:index'))
			else:
				return HttpResponse("Your food_cloud account is disabled.")
		else:
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'food_cloud/login.html')


def restaurant_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				try:
					restaurant = RestaurantProfile.objects.get(user=user)
				except RestaurantProfile.DoesNotExist:
					return redirect(reverse('food_cloud:login'))
				login(request, user)
				return redirect(reverse('food_cloud:index_restaurant'))
			else:
				return HttpResponse("Your food_cloud account is disabled.")
		else:
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'food_cloud/login_restaurant.html')


@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('food_cloud:index'))


class ProfileView(View):
	def get_user_details(self, username):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return None
		user_profile = UserProfile.objects.get_or_create(user=user)[0]
		form = UserProfileForm(
			{'picture': user_profile.picture, 'isRestaurant': user_profile.isRestaurant})
		return (user, user_profile, form)

	@method_decorator(login_required)
	def get(self, request, username):
		try:
			(user, user_profile, form) = self.get_user_details(username)
		except TypeError:
			return redirect(reverse('food_cloud:index'))
		context_dict = {'user_profile': user_profile,
						'selected_user': user,
						'form': form}
		return render(request, 'food_cloud/profile.html', context_dict)

	@method_decorator(login_required)
	def post(self, request, username):
		try:
			(user, user_profile, form) = self.get_user_details(username)
		except TypeError:
			return redirect(reverse('food_cloud:index'))
		form = UserProfileForm(
			request.POST, request.FILES, instance=user_profile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('food_cloud:profile', user.username)
		else:
			print(form.errors)
		context_dict = {'user_profile': user_profile,
						'selected_user': user,
						'form': form}
		return render(request, 'food_cloud/profile.html', context_dict)


class ProfileView_restaurant(View):
	def get_user_details(self, username):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return None
		user_profile = RestaurantProfile.objects.get_or_create(user=user)[0]
		form = RestaurantProfileForm({'average_rating': user_profile.average_rating,
									  'type': user_profile.type, 'isRestaurant': user_profile.isRestaurant})
		return (user, user_profile, form)

	@method_decorator(login_required)
	def get(self, request, username):
		try:
			(user, user_profile, form) = self.get_user_details(username)
		except TypeError:
			return redirect(reverse('food_cloud:index_restaurant'))
		context_dict = {'user_profile': user_profile,
						'selected_user': user,
						'form': form}
		return render(request, 'food_cloud/profile_restaurant.html', context_dict)

	@method_decorator(login_required)
	def post(self, request, username):
		try:
			(user, user_profile, form) = self.get_user_details(username)
		except TypeError:
			return redirect(reverse('food_cloud:index_restaurant'))
		form = RestaurantProfileForm(
			request.POST, request.FILES, instance=user_profile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('food_cloud:profile_restaurant', user.username)
		else:
			print(form.errors)
		context_dict = {'user_profile': user_profile,
						'selected_user': user,
						'form': form}
		return render(request, 'food_cloud/profile_restaurant.html', context_dict)


def about(request):
	context_dict = {}
	context_dict['boldmessage'] = 'This project was put together by Krasimir Ivanov, Jude Campbell, Olalekan Akala and Peter Rabai'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'food_cloud/about.html', context=context_dict)
	return response


def about_restaurant(request):
	context_dict = {}
	context_dict['boldmessage'] = 'This project was put together by Krasimir Ivanov, Jude Campbell, Olalekan Akala and Peter Rabai'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(
		request, 'food_cloud/about_restaurant.html', context=context_dict)
	return response


def contact(request):
	context_dict = {}
	context_dict['boldmessage'] = 'Contact us page(WIP)'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'food_cloud/contact.html', context=context_dict)
	return response


def contact_restaurant(request):
	context_dict = {}
	context_dict['boldmessage'] = 'Contact us page(WIP)'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(
		request, 'food_cloud/contact_restaurant.html', context=context_dict)
	return response


def my_account(request):
	context_dict = {}
	context_dict['boldmessage'] = 'my_account(WIP)'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'food_cloud/my_account.html',
					  context=context_dict)
	return response


def add_meal(request):
	user = request.user
	form = MealForm()
	restaurant = RestaurantProfile.objects.get_or_create(user=user)
	restaurant_slug = slugify(request.user.username)
	if request.method == 'POST':
		#form = MealForm(request.POST, restaurant_slug=slugify(request.user.username))
		form = MealForm(request.POST)
		if form.is_valid():
			candidate=form.save(commit=False)
			candidate.restaurant_slug=slugify(request.user.username)
			candidate.save()
			# restaurant_slug=restaurant_slug
			# form.save(commit=True)
			return redirect('/food_cloud/index_restaurant/')
		else:
			print(form.errors)
	return render(request, 'food_cloud/add_meal.html', {'form': form})


def search(request):
	result_list = []
	query = ""
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	print("DEBUG query=" + query)
	return render(request, 'food_cloud/search.html', {'result_list': result_list, 'query': query})


def search_restaurant(request):
	result_list = []
	query = ""
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	print("DEBUG query=" + query)
	return render(request, 'food_cloud/search_restaurant.html', {'result_list': result_list, 'query': query})


def search_restaurants(request):
	result_list = None
	query = ""
	if request.method == 'POST':
		query = request.POST['query']
		if query:
			result_list = RestaurantProfile.objects.filter(
				restaurant_name__contains=query)

			print(result_list)
	print("DEBUG query=" + query)
	return render(request, 'food_cloud/search_restaurants.html', {'result_list': result_list, 'query': query})


def show_meal(request, meal_name_slug):
	context_dict = {}
	try:
		meal = Meal.objects.get(slug=meal_name_slug)
		context_dict['meal'] = meal
	except Meal.DoesNotExist:
		context_dict['meal'] = None
	return render(request, 'food_cloud/meal.html', context=context_dict)


def show_restaurant(request, restaurant_name_slug):
	context_dict = {}
	try:
		restaurant = RestaurantProfile.objects.get(slug=restaurant_name_slug)
		context_dict['restaurant'] = restaurant
		meals = Meal.objects.filter(
			restaurant_slug=restaurant_name_slug)
		favourites = Favourite.objects.filter(
			meal__restaurant_slug=restaurant_name_slug)
		context_dict['favourites'] = favourites

		result = []
		for meal in meals:
			if any(x.meal.meal_id == meal.meal_id for x in favourites) != True:
				result.append(meal)
		context_dict['not_favourites'] = result
	except Restaurant.DoesNotExist:
		context_dict['restaurant'] = None
		context_dict['not_favourites'] = None
		context_dict['favourites'] = None
	return render(request, 'food_cloud/restaurant.html', context=context_dict)


@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")


def get_server_side_cookie(request, cookie, default_val=None):
	val = request.COOKIES.get(cookie)
	try:
		int(val)
	except (ValueError, TypeError):
		val = default_val
	return val


def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	last_visit_cookie = get_server_side_cookie(
		request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(
		last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		# Update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		# Set the last visit cookie
		request.session['last_visit'] = last_visit_cookie

	# Update/set the visits cookie
	request.session['visits'] = visits


@login_required
def add_order(request, meal_slug, meal_restaurant):
	amount = request.GET.get('amount', None)
	print(amount)
	if amount is not None:
		meal = Meal.objects.get(
			slug=meal_slug, restaurant_slug=meal_restaurant)
		user = UserProfile.objects.get(user=request.user)
		order = Order.objects.create(
			meal=meal, customer=user, amount=amount, date=datetime.now())
		data = {'success': True}
	else:
		data = {'success': False}
	return JsonResponse(data)


@login_required
def add_favourite(request, meal_name_slug):
	meal = Meal.objects.get(slug=meal_name_slug)
	user = UserProfile.objects.get(user=request.user)
	favourite = Favourite.objects.create(
		meal=meal, customer=user)
	favourite.save()
	return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_favourite(request, meal_name_slug):
	meal = Meal.objects.get(slug=meal_name_slug)
	instance = Favourite.objects.filter(meal__slug=meal_name_slug)
	instance.delete()
	return redirect(request.META.get('HTTP_REFERER'))


@login_required
def rate_meal(request, meal_slug, meal_restaurant):
	rating_value = request.GET.get('rating', None)
	print(rating_value)
	data = {}
	if rating_value is not None:
		try:
			rating_value = int(rating_value)
			meal = Meal.objects.get(
				slug=meal_slug, restaurant_slug=meal_restaurant)
			user = UserProfile.objects.get(user=request.user)
			rating, created = Rating.objects.get_or_create(
				meal=meal, customer=user)
			rating.rating = rating_value
			rating.save()
			data = {'success': True}
		except ValueError:
			data = {'success': False, 'error': 'Enter Integer'}
	else:
		data = {'success': False}
	return JsonResponse(data)


def get_context_dict(request):
	context_dict = {}
	if request.user.is_authenticated:
		try:
			user = UserProfile.objects.get(user=request.user)
		except UserProfile.DoesNotExist:
			user = None
		if user is not None:
			context_dict['orders'] = Order.objects.filter(
				customer=UserProfile.objects.get(user=request.user)).order_by('-date')[:5]
			context_dict['favorites'] = Favourite.objects.filter(
				customer=UserProfile.objects.get(user=request.user))[:5]

	return context_dict
