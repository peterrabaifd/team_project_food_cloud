from django import forms
from food_cloud.models import *
from django.contrib.auth.models import User
from food_cloud.models import UserProfile

class MealForm(forms.ModelForm):
	meal_id = forms.IntegerField(initial=0)
	meal_name = forms.CharField(max_length=30,
	help_text="Please enter the meal name.")
	description = forms.CharField(max_length=200)
	price = forms.IntegerField(initial=0)
	restaurant_id = forms.IntegerField(initial=0)
	picture = forms.ImageField()
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Meal
		fields = ('meal_name',)

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
	help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	# An inline class to provide additional information on the form.
	class Meta:
		# Provide an association between the ModelForm and a model
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data
		
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('email_address', 'picture', 'isCompany')