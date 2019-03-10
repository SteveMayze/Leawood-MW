from .base import FunctionalTest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from unittest import skip


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

		self.check_placeholder( 'id_user_name', 'Enter your user ID')
		self.check_placeholder( 'id_password', 'Enter your password')

		# He does not know any credentials, so he cancels the dialog.
		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[1]/div/div/div/div[3]/button[1]"))).click()
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
		self.check_placeholder( 'id_registration_password', 'Enter your password')
		self.check_placeholder( 'id_registration_password2', 'Confirm your password')

		# Graeme enters his (minimal) registration
		self.browser.find_element_by_id('id_registration_username').send_keys('graeme')
		self.browser.find_element_by_id('id_registration_password').send_keys('welcome1')
		self.browser.find_element_by_id('id_registration_password2').send_keys('welcome1')

		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[2]/div/div/div/div[3]/button[2]"))).click()
		# -- The strange work around from above is not needed here.
		# Graeme sees that the registration and sign on have gone and are replaced with
		# The link to sign on.
		self.wait_for_modal_close( 'id_registerModal' )
		self.wait_for(lambda: self.browser.find_element_by_link_text('Sign off'))
		self.assertIn('Registration was successful', self.browser.find_elements_by_class_name('messages')[0].text)

		# Graeme signs off to see if he can sign on again.
		self.browser.find_element_by_link_text('Sign off').click()
		self.wait_for(lambda: self.browser.find_element_by_link_text('Register'))

	def test_can_not_register_again( self ):
		# Graeme is curious to know what happes when he attempts to register again
		self.browser.get(self.live_server_url)

		# Goes back into the registration form. 
		register_link = self.browser.find_element_by_link_text('Register').click()

		# The modal dialog opens and he enters the same details again
		login_dialog = self.browser.find_element_by_id('id_registerModal')
		self.assertIn('show', login_dialog.get_attribute('class'))
		self.browser.find_element_by_id('id_registration_username').send_keys('graeme')
		self.browser.find_element_by_id('id_registration_password').send_keys('welcome1')
		self.browser.find_element_by_id('id_registration_password2').send_keys('welcome1')
		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[2]/div/div/div/div[3]/button[2]"))).click()

		# Graeme see that he is not signed in and there is a warning that the name
		# is already taken.
		# --- This could be JavaScript i.e. Ajax to verify the user name
		self.assertIn('The name is already in use', self.browser.find_elements_by_class_name('messages')[0].text)




	@skip("Skipping for the moment - until the Authentication is complete")
	def test_can_sign_in(self):
		# First, he has to sign in. He clicks on the sign in link and
		# a Modal dialog appears asking for his credentials.
		self.browser.get(self.live_server_url)

		signin_link = self.browser.find_element_by_link_text('Sign in')
		signin_link.click()
		time.sleep(1)
		user_name = self.browser.find_element_by_id('id_user_name')
		self.assertEqual(user_name.get_attribute('placeholder'), 'Enter your user ID')



		user_name.send_keys('graeme')
		password = self.browser.find_element_by_id('id_password')
		self.assertEqual(password.get_attribute('placeholder'), 'Enter your password')
		password.send_keys('welcome1')
		password.send_keys(Keys.ENTER)
		self.wait_for_link('Sign off')
		self.assertIn('Sign on successful', self.browser.find_element_by_id('id_messages').text)


# Graeme forgets his password