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
		_username = registration_form['username'].value()
		_password = registration_form['password'].value()
		try:
			user = User.objects.get( username=_username )
			messages.error(
				request,
				f'The username "{_username}" is already taken.',
				extra_tags="error-message"
			)
		except User.DoesNotExist:
			user = User(username=_username)
			user.set_password(_password)
			user.save()
			messages.success(
				request,
				"Registration was successful.",
				extra_tags="success-message"
			)
			request.session['username'] = _username
			user = auth.authenticate(username=_username, password=_password)
			if user:
				auth.login(request, user)

	return redirect('/')


def login( request ):
	username = request.POST['username']
	password = request.POST['password']
	request.session['username'] = username
	user = auth.authenticate(username=username, password=password)
	if user:
		auth.login(request, user)
		messages.success(
			request,
			"Login was successful."
		)
	else:
		messages.error(
			request,
			"Login was unsuccessful."
		)
	return render(request, 'dashboard/dashboard.html')


def logout( request ):
	auth.logout( request )
	return redirect('/')
