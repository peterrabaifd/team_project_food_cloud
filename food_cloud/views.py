from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
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


def index(request):
    context_dict = {}

    popular_meal_list = Meal.objects.order_by('-num_orders')
    context_dict['meals'] = popular_meal_list[:5]
    context_dict['visits'] = request.session['visits']
    context_dict['orders'] = Order.objects.order_by('-date')[:5]
    context_dict['restaurants'] = RestaurantProfile.objects.order_by(
        'restaurant_name')

    response = render(request, 'food_cloud/index.html', context=context_dict)
    return response


def index_restaurant(request):
    context_dict = {}
    # context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # context_dict['categories'] = category_list
    # context = RequestContext(request)

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
    form = MealForm()
    restaurant = RestaurantProfile.objects.get_or_create(user=request.user)
    restaurant_slug = restaurant[0].slug
    if request.method == 'POST':
        form = MealForm(request.POST, restaurant_slug=restaurant_slug)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/food_cloud/')
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
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.COOKIES.get(cookie)
    print(val)
    try:
        int(val)
    except (ValueError, TypeError):
        val = default_val
        print(val + " here")
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


def clear_amount_cookie(request):
    request.COOKIES['amount'] = '0'
    print("Done")


@login_required
def add_order(request, meal_slug, meal_restaurant):
    print("OK")
    amount = get_server_side_cookie(request, 'amount', '1')
    print(amount)
    # clear_amount_cookie(request)
    if amount is not None:
        meal = Meal.objects.get(
            slug=meal_slug, restaurant_slug=meal_restaurant)
        user = UserProfile.objects.get(user=request.user)
        order = Order.objects.create(
            meal=meal, customer=user, amount=amount, date=datetime.now())
        order.save()
        # clear_amount_cookie(request)
    return redirect('food_cloud:index')


@login_required
def add_favourite(request, meal_name_slug):
    meal = Meal.objects.get(slug=meal_name_slug)
    user = UserProfile.objects.get(user=request.user)
    favourite = Favourite.objects.create(
        meal=meal, customer=user)
    favourite.save()
    return redirect('food_cloud:show_restaurant', meal.restaurant_slug)


@login_required
def remove_favourite(request, meal_name_slug):
    meal = Meal.objects.get(slug=meal_name_slug)
    instance = Favourite.objects.filter(meal__slug=meal_name_slug)
    instance.delete()
    return show_restaurant(request, meal.restaurant_slug)
