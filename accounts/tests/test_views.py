from django.test import TestCase
import accounts.views


class RegisterViewTest(TestCase):

	def test_redirects_to_home_page(self):
		response = self.client.post('/accounts/register', data={
			'username': 'graeme@leawood.com',
			'password': 'welcome1'
			})
		self.assertRedirects(response, '/')


	# def test_register_creats_session_cookie(self):
	# 	response = self.client.post('/accounts/register', data={
	# 		'username': 'graeme@leawood.com',
	# 		'password': 'welcome1'
	# 		})




# class LoginViewTest