from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.shortcuts import render

User = get_user_model()

def register( request ):

	username = request.POST['username']
	request.session['username'] = username
	password = request.POST['password']

	try:
		user = User.objects.get(username=username)
		messages.error(
			request,
			"The username is already taken."
		)
	except User.DoesNotExist:
		user = User(username=username)
		user.set_password(password)
		user.save()
		messages.success(
			request,
			"Registration was successful."
		)


	return render(request, 'dashboard/dashboard.html')


def login( request ):
	try:	
		username = request.POST['username']
		password = request.POST['password']

		user = User.objects.get(username=username)
		request.session['username'] = username
	except User.DoesNotExist:
		messages.error(
			request,
			"Login was unsuccessful."
		)
	return render(request, 'dashboard/dashboard.html')


