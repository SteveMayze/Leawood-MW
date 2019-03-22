from accounts.forms import RegistrationForm, LoginForm
from accounts.models import Token
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
import uuid


User = get_user_model()


def register( request ):

	registration_form = RegistrationForm(request.POST)

	# username = request.POST['username']
	# request.session['username'] = username
	# password = request.POST['password']

	if registration_form.is_valid():
		_username = registration_form['username'].value()
		_email = registration_form['email'].value()
		_password = registration_form['password'].value()
		try:
			user = User.objects.get( username=_username )
			messages.error(
				request,
				f'The username "{_username}" is already taken.',
				extra_tags="error-message"
			)
		except User.DoesNotExist:
			user = User(username=_username, email=_email)
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
	# username = request.POST['username']
	# password = request.POST['password']

	login_form = LoginForm(request.POST)
	if login_form.is_valid():
		username = login_form['username'].value()
		password = login_form['password'].value()
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request, user)
			request.session['username'] = username
			messages.success(
				request,
				"Login was successful."
			)
		else:
			messages.error(
				request,
				"Login was unsuccessful."
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


def reset_password( request ):
	if request.method == 'POST':
		username = request.POST['username']
		email = User.objects.get(username=username).email
		uid = str(uuid.uuid4())
		token, created = Token.objects.get_or_create(username=username)
		token.uid = uid
		token.save()
		url = request.build_absolute_uri(f'/accounts/new_password?uid={uid}')
		send_mail(
			'Leawood password reset',
			f'Use this link to reset your password:\n\n{url}',
			'noreply@leawood.com.au',
			[ email ],
			)
		return render(request, 'accounts/reset_email_sent.html')
	return render(request, 'accounts/reset_password.html')

def new_password( request ):
	uid = ''
	if request.method == 'GET':
		uid = request.GET.get('uid')

	if request.method == 'POST':
		password = request.POST.get('password')
		uid = request.POST.get('token')
		token = Token.objects.get(uid=uid )
		user = User.objects.get(username=token.username)
		user.set_password(password)
		user = auth.authenticate(username=token.username, password=password)
		if user:
			auth.login(request, user)
			request.session['username'] = token.username
			messages.success(
				request,
				"Password was successfully changed."
			)
		else:
			messages.error(
				request,
				"Password was not reset correctly."
			)
		token.delete()			
		return redirect('/')
	return render(request, 'accounts/new_password.html', {'token': uid})	