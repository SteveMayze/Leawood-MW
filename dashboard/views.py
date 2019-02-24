from django.shortcuts import render
from django.http import HttpResponse
from accounts.forms import RegistrationForm

def dashboard(request):
	registration_form = RegistrationForm(request.POST)
	return render(request, 'dashboard/dashboard.html', {'registration_form': registration_form})