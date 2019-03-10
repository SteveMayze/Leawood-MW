from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.shortcuts import render
from accounts.forms import RegistrationForm

User = get_user_model()

def register( request ):

	registration_form = RegistrationForm(request.POST)

	# username = request.POST['username']
	# request.session['username'] = username
	# password = request.POST['password']

	if registration_form.is_valid():
		username = registration_form['username'].value()
		password = registration_form['password'].value()
		try:
			user = User.objects.get(username=username)
			messages.error(
				request,
				"The username is already taken.",
				extra_tags="error-message"
			)
		except User.DoesNotExist:
			user = User(username=username)
			user.set_password(password)
			user.save()
			messages.success(
				request,
				"Registration was successful.",
				extra_tags="success-message"
			)
			request.session['username'] = username
			user = auth.authenticate(username=username, password=password)
			if user:
				auth.login(request, user)
	return redirect('/')


def login( request ):
	try:	
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.get(username=username)
		request.session['username'] = username
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request, user)
	except User.DoesNotExist:
		messages.error(
			request,
			"Login was unsuccessful."
		)
	return render(request, 'dashboard/dashboard.html')


