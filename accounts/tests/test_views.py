
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.test import TestCase
from importlib import import_module
import accounts.views
from accounts.models import Token
from unittest.mock import patch, call
from unittest import skip

User = get_user_model()

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
Session = SessionStore.get_model_class()

TEST_EMAIL = "smayze@yahoo.com"

class RegisterViewTest(TestCase):


	# def setUp( self ):
	#	User.objects.create(username="def", password="1234")

	def test_register_uses_homepage(self):
		response = self.client.post('/accounts/register', data={
			'username': 'abc',
			'email': 'abc@def.com',
			'password': 'welcome1',
			'password2': 'welcome1'

			})
		self.assertEqual(302, response.status_code)
		# self.assertTemplateUsed(response, 'dashboard/dashboard.html')


	def test_register_creates_session_cookie(self):
		response = self.client.post('/accounts/register', data={
			'username': 'abc',
			'email': 'abc@def.com',
			'password': 'welcome1',
			'password2': 'welcome1'

			})
		response.has_header('csrftoken')


	def test_session_cookie_contains_username(self):
		self.client.post('/accounts/register', data={
			'username': 'abc',
			'email': 'abc@def.com',
			'password': 'welcome1',
			'password2': 'welcome1'
			})
		session_key = Session.objects.all()[0].session_key
		session = SessionStore(session_key=session_key)
		self.assertEqual('abc', session['username'])


	def test_registration_creates_new_user(self):
		self.client.post('/accounts/register', data={
			'username': 'abc',
			'email': 'abc@def.com',
			'password': 'welcome1',
			'password2': 'welcome1'
			})
		user = User.objects.get(username='abc')

		self.assertEqual('abc', user.username)
		self.assertEqual('abc@def.com', user.email)
		self.assertNotEqual('welcome1', user.password)



	@patch('accounts.views.messages')
	def test_registration_username_must_be_unique(self, mock_messages):
		User.objects.create(username="def", password="1234")
		response = self.client.post('/accounts/register', data={
			'username': 'def',
			'email': 'abc@def.com',
			'password': 'welcome1',
			'password2': 'welcome1'
			})
		self.assertTrue(mock_messages.error.called)




	@patch('accounts.views.auth')
	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		response = self.client.post('/accounts/register', data={
			'username': 'abc',
			'email': 'abc@def.com',
			'password': 'welcome1',
			'password2': 'welcome1'
			})
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(username='abc', password='welcome1')		
		)



class LoginViewTest(TestCase):

	def test_login_uses_homepage(self):
		response = self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		self.assertEqual(200, response.status_code)
		self.assertTemplateUsed(response, 'dashboard/dashboard.html')


	def test_login_user_must_exist(self):
		response = self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		message = list(response.context['messages'])[0]
		self.assertEqual(
			message.message,
			"Login was unsuccessful."
		)
		# self.assertEqual(message.tags, "error")


	def test_login_creates_session_cookie(self):
		response = self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		response.has_header('csrftoken')


	def test_login_cookie_contains_username(self):
		user = User.objects.create(username='abc')
		user.set_password("welcome1")
		user.save()
		self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		session_key = Session.objects.all()[0].session_key
		session = SessionStore(session_key=session_key)
		self.assertEqual('abc', session['username'])

	@patch('accounts.views.auth')
	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		User.objects.create(username='abc')
		response = self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(username='abc', password='welcome1')		
		)

	@patch('accounts.views.auth')
	def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
		User.objects.create(username='abc')
		response = self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		self.assertEqual(
			mock_auth.login.call_args,
			call(response.wsgi_request, mock_auth.authenticate.return_value)
		)

class LogoutTest( TestCase ):
	def test_logout_uses_homepage(self):
		response = self.client.post('/accounts/logout')
		self.assertEqual(302, response.status_code)
		## self.assertTemplateUsed(response, 'dashboard/dashboard.html')


	@patch('accounts.views.auth')
	def test_signoff_returns_to_dashboard(self, mock_auth):
		self.client.post('/accounts/logout')
		self.assertTrue(mock_auth.logout.called)

class ResetPasswordViewTest( TestCase ):

	def test_uses_reset_password_page( self ):
		user_ = User.objects.create(username='abc', email=TEST_EMAIL)
		user_.set_password('welcome1')
		user_.save()
		response = self.client.post('/accounts/reset_password', data={
			'username': 'abc'
		})
		self.assertEqual(200, response.status_code)
		self.assertTemplateUsed(response, 'accounts/reset_email_sent.html')

class NewPasswordViewTest( TestCase ):

	def test_new_password_uses_correct_template( self ):
		user_ = User.objects.create(username = 'abc', email=TEST_EMAIL)
		user_.set_password("welcome1")
		user_.save()
		token_ = Token.objects.create(username = 'abc', uid="123")
		response = self.client.get('/accounts/new_password?token=123')	
		self.assertTemplateUsed(response, 'accounts/new_password.html')

	def test_session_cookie_container_username( self ):
		user_ = User.objects.create(username = 'abc', email=TEST_EMAIL)
		user_.set_password("welcome1")
		user_.save()
		token_ = Token.objects.create(username = 'abc', uid="123")

		response = self.client.post('/accounts/new_password', data = {
			'password': 'welcome1',
			'password2': 'welcome1'
		})	
		session_key = Session.objects.all()[0].session_key
		session = SessionStore(session_key=session_key)
		self.assertEqual('abc', session['username'])
