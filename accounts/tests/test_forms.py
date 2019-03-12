from django.test import TestCase

from django.contrib.auth import get_user_model
from accounts.forms import (
	PASSWORDS_DONT_MATCH, 
	RegistrationForm,
	LoginForm
)

User = get_user_model()


class RegistrationFormTest(TestCase):

	def test_validation_fails_if_passwords_dont_match(self):
		form = RegistrationForm(data={
			'username': 'abc', 
			'password': 'welcome1', 
			'password2': 'welcome2'
		})

		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['password2'], [PASSWORDS_DONT_MATCH])

	def test_validation_passes_if_pwd_match(self):
		form = RegistrationForm(data={
			'username': 'abc', 
			'password': 'welcome1', 
			'password2': 'welcome1'
		})

		self.assertTrue(form.is_valid())

class LoginFormTest( TestCase ):

	def test_can_login_with_form( self ):
		form = LoginForm( data = { 
			'username': 'abc',
			'password': 'welcome1'
		})

		self.assertEqual( 'abc', form['username'].value())		
		self.assertEqual( 'welcome1', form['password'].value())

	def test_values_can_not_be_empty( self ):
		form = LoginForm( data = { 
			'username': '',
			'password': ''
		})

		self.assertFalse(form.is_valid())
