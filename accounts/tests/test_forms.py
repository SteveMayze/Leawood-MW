from django.test import TestCase

from django.contrib.auth import get_user_model
from accounts.forms import (
	PASSWORDS_DONT_MATCH, 
	RegistrationForm
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
