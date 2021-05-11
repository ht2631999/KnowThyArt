from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Activities
from my_project import settings

 

select_activity = []
for act in Activities.objects.all():
	select_activity.append((act.activity, act.activity))

user_types = [ ('Organiser','Organiser'), ('Participant','Participant')]

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
	medical_history = forms.CharField(widget=forms.Textarea)
	activities = forms.Select(choices=select_activity)
	class Meta:
		model = User

		fields= ['username','email','date_of_birth', 'activities', 'medical_history','password1','password2']



class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
	medical_history = forms.CharField(widget=forms.Textarea)
	activities = forms.Select(choices=select_activity)

	class Meta:
		model = User

		fields= ['username','email','date_of_birth', 'activities', 'medical_history']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']
