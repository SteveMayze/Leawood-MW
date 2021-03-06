
from .base import FunctionalTest, TEST_EMAIL
from django.contrib.auth import get_user_model
from django.core import mail
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from unittest import skip
import re
import time

User = get_user_model()

SUBJECT = "Leawood password reset"
class LoginTest(FunctionalTest):


	def test_can_open_signin(self):
		# Graeme comes to the PC and opens the Leawood App by going to 
		# http://host/leawood

		self.browser.get(self.live_server_url)

		# He sees the main menu bar. Since he is not signed in, there is only
		# the dashboard tab and an option to sign in at the top.
		# TODO
		self.wait_for_modal_close( 'id_loginModal' )

		signin_link = self.browser.find_element_by_link_text('Sign in')
		self.assertTrue(signin_link)

		# He tries to sign in
		signin_link.click()
		# and sees that a Model dialog appears and requests a user name
		# and password
		# login_dialog = self.browser.find_element_by_id('id_loginModal')
		self.wait_for_modal_show('id_loginModal')
		# self.assertIn('show', login_dialog.get_attribute('class'))

		self.check_placeholder( 'id_login_username', 'Enter your user ID')
		self.check_placeholder( 'id_login_password', 'Enter your password')

		# He does not know any credentials, so he cancels the dialog.
		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_loginModal"]/div/div/div[3]/button[1]'))).click()

		# This is a strange work around to dismiss a modal dialog
		# cancel_button = self.browser.find_element_by_xpath("/html/body/form/div/div/div/div[3]/button[1]")
		# cancel_button.click()
		login_dialog = self.browser.find_element_by_id('id_loginModal')
		login_dialog.send_keys(Keys.ESCAPE)
		self.wait_for_modal_close( 'id_loginModal' )


	def test_can_register(self):
		self.browser.get(self.live_server_url)

		# He now sees the Register button and clicks that. 
		register_link = self.browser.find_element_by_link_text('Register').click()

		# Another Modal dialog appears that asks for the user details and
		# to register a password.

		login_dialog = self.browser.find_element_by_id('id_registerModal')
		self.assertIn('show', login_dialog.get_attribute('class'))

		self.check_placeholder( 'id_registration_username', 'Enter your user ID')
		self.check_placeholder( 'id_registration_email', 'your.email@address.com')
		self.check_placeholder( 'id_registration_password', 'Enter your password')
		self.check_placeholder( 'id_registration_password2', 'Confirm your password')

		# Graeme enters his (minimal) registration
		self.browser.find_element_by_id('id_registration_username').send_keys('graeme')
		self.browser.find_element_by_id('id_registration_email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_id('id_registration_password').send_keys('welcome1')
		self.browser.find_element_by_id('id_registration_password2').send_keys('welcome1')

		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_registerModal"]/div/div/div[3]/button[2]'))).click()
		# -- The strange work around from above is not needed here.
		# Graeme sees that the registration and sign on have gone and are replaced with
		# The link to sign on.
		self.wait_for_modal_close( 'id_registerModal' )
		self.wait_for_link('Sign off')
		self.assertIn('Registration was successful', self.browser.find_elements_by_class_name('messages')[0].text)

		# Graeme signs off to see if he can sign on again.
		self.browser.find_element_by_link_text('Sign off').click()
		self.wait_for(lambda: self.browser.find_element_by_link_text('Register'))

		# Goes back into the registration form. 
		register_link = self.browser.find_element_by_link_text('Register').click()

		# The modal dialog opens and he enters the same details again
		login_dialog = self.browser.find_element_by_id('id_registerModal')
		self.assertIn('show', login_dialog.get_attribute('class'))
		self.browser.find_element_by_id('id_registration_username').send_keys('graeme')
		self.browser.find_element_by_id('id_registration_email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_id('id_registration_password').send_keys('welcome1')
		self.browser.find_element_by_id('id_registration_password2').send_keys('welcome1')
		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_registerModal"]/div/div/div[3]/button[2]'))).click()
		# Graeme see that he is not signed in and there is a warning that the name
		# is already taken.
		# --- This could be JavaScript i.e. Ajax to verify the user name
		self.assertIn(f'The username "graeme" is already taken', self.browser.find_elements_by_class_name('messages')[0].text)

		# Graeme finds himself back to needing to log in again
		self.wait_for(lambda: self.browser.find_element_by_link_text('Register'))



	def test_can_sign_in(self):
		# First, he has to sign in. He clicks on the sign in link and
		# a Modal dialog appears asking for his credentials.
		test_user = self.create_user('graeme', 'welcome1', TEST_EMAIL)

		self.browser.get(self.live_server_url)

		signin_link = self.browser.find_element_by_link_text('Sign in')
		signin_link.click()

		login_dialog = self.browser.find_element_by_id('id_loginModal')
		self.assertIn('show', login_dialog.get_attribute('class'))


		user_name = self.browser.find_element_by_id('id_login_username')
		self.assertEqual(user_name.get_attribute('placeholder'), 'Enter your user ID')

		user_name.send_keys('graeme')
		password = self.browser.find_element_by_id('id_login_password')
		self.assertEqual(password.get_attribute('placeholder'), 'Enter your password')
		password.send_keys('welcome1')
		password.send_keys(Keys.ENTER)
		self.wait_for_link('Sign off')
		self.assertIn('Login was successful.', self.browser.find_elements_by_class_name('messages')[0].text)


	def test_user_can_reset_password( self ):
		test_user = self.create_user('graeme', 'welcome1', TEST_EMAIL)

		self.browser.get(self.live_server_url)
		# Graeme attempts to sign in after a long while and realises he
		# has forgotten his password.

		# He clicks on the Sign in
		signin_link = self.browser.find_element_by_link_text('Sign in')
		signin_link.click()
		# ... and sees a "forgot password link" and clicks it.
		forgotten_password_link = self.browser.find_element_by_link_text('Forgotten password?')
		forgotten_password_link.click()

		# He is directed to a completely new page where he can enter
		# his email address
		self.wait_for(lambda: self.browser.find_element_by_id('id_username'))

		# He enters his username and clicks send.
		username_input = self.browser.find_element_by_id('id_username')
		username_input.send_keys('graeme')
		reset_password_button = self.browser.find_element_by_id('id_send_email')

		reset_password_button.submit()
		
		# A secret token is generated and stored with the users 
		# email address (lookup the username) and send it to them
		# -  This needs to be linked to the user name so the registration 
		#    will now require a valid email address

		self.wait_for(lambda: self.assertIn(
			'Check your email. You will find a message with a link to reset your password',
			self.browser.find_element_by_tag_name('body').text
		))

		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(SUBJECT, email.subject)

		# He has to check his email where there is a link containing that token

		self.assertIn('Use this link to reset your password', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(f'Could not find the url in the email body:\n{email.body}')
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)

		# When he clicks on the link, the token is checked and they will be 
		# directed to another page where he can set a new password.
		self.browser.get(url)
		self.wait_for(lambda: self.browser.find_element_by_id('id_reset_password1'))

		# Graene enters a new password twice
		password1 = self.browser.find_element_by_id('id_reset_password1')
		password1.send_keys("welcome1")
		password2 = self.browser.find_element_by_id('id_reset_password2')
		password2.send_keys("welcome1")

		set_password_btn = self.browser.find_element_by_id('id_set_password')
		set_password_btn.submit()


		# Once he sets a new password, he is automatically logged in and 
		# directed back to the home page.
		self.wait_for_link('Sign off')
		self.assertIn('Password was successfully changed.', self.browser.find_elements_by_class_name('messages')[0].text)


# Verification that the token can expire.

