
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.test import TestCase
from importlib import import_module
import accounts.views

User = get_user_model()

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
Session = SessionStore.get_model_class()

class RegisterViewTest(TestCase):

	def test_register_uses_homepage(self):
		response = self.client.post('/accounts/register', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		self.assertEqual(200, response.status_code)
		self.assertTemplateUsed(response, 'dashboard/dashboard.html')


	def test_register_creates_session_cookie(self):
		response = self.client.post('/accounts/register', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		response.has_header('csrftoken')


	def test_session_cookie_contains_username(self):
		self.client.post('/accounts/register', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		session_key = Session.objects.all()[0].session_key
		session = SessionStore(session_key=session_key)
		self.assertEqual('abc', session['username'])


	def test_registration_creates_new_user(self):
		self.client.post('/accounts/register', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		user = User.objects.all()[0]

		self.assertEqual('abc', user.username)
		self.assertNotEqual('welcome1', user.password)


	def test_registration_username_must_be_unique(self):
		user = User.objects.create(username="abc")
		response = self.client.post('/accounts/register', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		message = list(response.context['messages'])[0]
		self.assertEqual(
			message.message,
			"The username is already taken."
		)
		self.assertEqual(message.tags, "error")





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
		self.assertEqual(message.tags, "error")


	def test_login_creates_session_cookie(self):
		response = self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		response.has_header('csrftoken')


	def test_login_cookie_contains_username(self):
		User.objects.create(username='abc')
		self.client.post('/accounts/login', data={
			'username': 'abc',
			'password': 'welcome1'
			})
		session_key = Session.objects.all()[0].session_key
		session = SessionStore(session_key=session_key)
		self.assertEqual('abc', session['username'])


