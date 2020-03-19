from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from food_cloud.models import *
from food_cloud.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from food_cloud.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from food_cloud.bing_search import run_query
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.decorators import method_decorator

def index(request):
	context_dict = {}
	#context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
	#context_dict['categories'] = category_list
	#context = RequestContext(request)
	
	meal_list = Meal.objects.order_by('meal_name')
	
	context_dict = {}
	context_dict['meals'] = meal_list
	
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(request, 'food_cloud/index.html', context=context_dict)
	return response
	
def index_restaurant(request):
	context_dict = {}
	#context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
	#context_dict['categories'] = category_list
	#context = RequestContext(request)
	
	meal_list = Meal.objects.order_by('meal_name')
	
	context_dict = {}
	context_dict['meals'] = meal_list
	
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(request, 'food_cloud/index_restaurant.html', context=context_dict)
	return response
	
def register_choice(request):
	context_dict = {}
	response = render(request, 'food_cloud/register_choice.html', context=context_dict)
	return response
	
def login_choice(request):
	context_dict = {}
	response = render(request, 'food_cloud/login_choice.html', context=context_dict)
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
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'food_cloud/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
	
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
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = RestaurantForm()
		profile_form = RestaurantProfileForm()
	return render(request, 'food_cloud/register_restaurant.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
	
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
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
		form = UserProfileForm({'picture': user_profile.picture, 'isRestaurant': user_profile.isRestaurant})
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
		form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
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
		form = RestaurantProfileForm({'average_rating': user_profile.average_rating,'type': user_profile.type, 'isRestaurant': user_profile.isRestaurant})
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
		form = RestaurantProfileForm(request.POST, request.FILES, instance=user_profile)
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
	context_dict['boldmessage'] = 'This project was put together by Peter Rabai'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'food_cloud/about.html', context=context_dict)
	return response
	
def contact(request):
	context_dict = {}
	context_dict['boldmessage'] = 'Contact us page(WIP)'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'food_cloud/contact.html', context=context_dict)
	return response
	
def my_account(request):
	context_dict = {}
	context_dict['boldmessage'] = 'my_account(WIP)'
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'food_cloud/my_account.html', context=context_dict)
	return response
	
def add_meal(request):
	form = MealForm()
	if request.method == 'POST':
		form = MealForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return redirect('/food_cloud/')
		else:
			print(form.errors)
	return render(request, 'food_cloud/add_meal.html', {'form': form})
	
def search(request):
	result_list = []
	query=""
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	print("DEBUG query=" + query)
	return render(request, 'food_cloud/search.html', {'result_list': result_list, 'query': query})
	
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
		restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
		context_dict['restaurant'] = restaurant
	except Restaurant.DoesNotExist:
		context_dict['restaurant'] = None
	return render(request, 'food_cloud/restaurant.html', context=context_dict)
	
def show_category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	return render(request, 'food_cloud/category.html', context=context_dict)

@login_required	
def add_category(request):
	form = CategoryForm()
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)
			# Now that the category is saved, we could confirm this.
			# For now, just redirect the user back to the index view.
			return redirect('/food_cloud/')
		else:
			# The supplied form contained errors -
			# just print them to the terminal.
			print(form.errors)
	# Will handle the bad form, new form, or no form supplied cases.
	# Render the form with error messages (if any).
	return render(request, 'food_cloud/add_category.html', {'form': form})

@login_required	
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except:
		category = None
	
	# You cannot add a page to a Category that does not exist... DM
	if category is None:
		return redirect('/food_cloud/')

	form = PageForm()

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()

				return redirect(reverse('food_cloud:show_category', kwargs={'category_name_slug': category_name_slug}))

				
			else:
				print(form.errors)
	
	context_dict = {'form': form, 'category': category}
	return render(request, 'food_cloud/add_page.html', context=context_dict)
	
@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val	
	
def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
	
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