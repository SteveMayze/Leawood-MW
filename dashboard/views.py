from django.shortcuts import render
from django.http import HttpResponse
from accounts.forms import RegistrationForm, LoginForm

def dashboard(request):
	registration_form = RegistrationForm(request.POST)
	login_form = LoginForm(request.POST)
	return render(request, 'dashboard/dashboard.html', {
		'registration_form': registration_form,
		'login_form': login_form
	})