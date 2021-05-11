from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'Your Account Has Been Created!  You can now login')
			return redirect('login')
		context={
				'form': form,
				'title': 'Register'
		}

	else:
		form = UserRegisterForm()
		context={
				'form': form,
				'title': 'Register'
		}
	return render(request,'users/register.html',context)


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance= request.user) 	#user update form instance
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile) #profile update form instance

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()

			messages.success(request, f'Your Profile Has Been Updated!')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance= request.user) 	#user update form instance
		p_form = ProfileUpdateForm(instance= request.user.profile) #profile update form instance
	

	
	context = {
	'u_form' : u_form,
	'p_form' : p_form,
	'title' : 'Profile'
	}
	return render(request, 'users/profile.html',context)
