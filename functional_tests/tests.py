from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_WAIT = 10;

class newVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_modal(self, modal_id):
		start_time = time.time()
		while True:
			try:
				model = self.browser.find_element_by_id(modal_id)
				self.assertEqual('true', model.get_attribute('aria-hidden'))
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def check_placeholder(self, element_id, value):
		element = self.browser.find_element_by_id(element_id)
		self.assertEqual(element.get_attribute('placeholder'), value)




	def test_can_see_the_dashboard(self):
		# Graeme comes to the PC and opens the Leawood App by going to 
		# http://host/leawood

		self.browser.get(self.live_server_url)
		assert 'Leawood' in self.browser.title

		# He sees the main menu bar. Since he is not signed in, there is only
		# the dashboard tab and an option to sign in at the top.
		# TODO
		self.wait_for_modal( 'id_loginModal' )

		signin_link = self.browser.find_element_by_link_text('Sign in')
		self.assertTrue(signin_link)

		# He tries to sign in
		signin_link.click()
		# and sees that a Model dialog appears and requests a user name
		# and password
		login_dialog = self.browser.find_element_by_id('id_loginModal')
		self.assertIn('show', login_dialog.get_attribute('class'))

		self.check_placeholder( 'id_user_name', 'Enter your user ID')
		self.check_placeholder( 'id_password', 'Enter your password')

		# He does not know any credentials, so he cancels the dialog.
		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[1]/div/div/div/div[3]/button[1]"))).click()
		# This is a strange work around to dismiss a modal dialog
		# cancel_button = self.browser.find_element_by_xpath("/html/body/form/div/div/div/div[3]/button[1]")
		# cancel_button.click()
		login_dialog = self.browser.find_element_by_id('id_loginModal')
		login_dialog.send_keys(Keys.ESCAPE)
		self.wait_for_modal( 'id_loginModal' )

		# He now sees the Register button and clicks that. 
		register_link = self.browser.find_element_by_link_text('Register').click()

		# Another Modal dialog appears that asks for the user details and
		# to register a password.

		login_dialog = self.browser.find_element_by_id('id_registerModal')
		self.assertIn('show', login_dialog.get_attribute('class'))

		self.check_placeholder( 'id_user_name_register', 'Enter your user ID')
		self.check_placeholder( 'id_password1_register', 'Enter your password')
		self.check_placeholder( 'id_password2_register', 'Confirm your password')

		# Graeme enters his (minimal) registration
		self.browser.find_element_by_id('id_user_name_register').send_keys('graeme')
		self.browser.find_element_by_id('id_password1_register').send_keys('welcome1')
		self.browser.find_element_by_id('id_password2_register').send_keys('welcome1')

		WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form[2]/div/div/div/div[3]/button[2]"))).click()
		# The strange work around from above is not needed here.
		# login_dialog = self.browser.find_element_by_id('id_registerModal')
		# login_dialog.send_keys(Keys.ENTER)
		self.wait_for_modal( 'id_registerModal' )

		# Once signed in, the other menu items become active

		# Locations

		# Devices

		# Register


		# ...

		# He also sees only the Dashboard that is in a view only mode.
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Dashboard', header_text)

		# The dashboard shows a graph for some of the devices.
		# TODO

		# There is a search area where the devices can be searched for and
		# the dashboard filtered for those/that specific device(s).
		searchbox = self.browser.find_element_by_id('id_search_filter')
		self.assertEqual(searchbox.get_attribute('placeholder'), 'device filter')

		# He wants to see only the Solar charges
		# Graeme enters "solar" into the search box
		searchbox.send_keys('solar')

		# When he hits ENTER, the list is reduced only devices with "solar"
		# in their name
		searchbox.send_keys(Keys.ENTER)
		time.sleep(1)

		device_table = self.browser.find_element_by_id('id_device_table')
		rows = device_table.find_elements_by_tag_name('tr')
		self.assertTrue(
			all('solar' in row.text.lower() for row in rows)
		)



		# Graeme signs on and sees that the menu has expanded to be able 
		# to manage the devices

		# First, he has to sign in. He clicks on the sign in link and
		# a Modal dialog appears asking for his credentials.
		signin_link.click()
		time.sleep(1)
		user_name = self.browser.find_element_by_id('id_user_name')
		self.assertEqual(user_name.get_attribute('placeholder'), 'Enter your user ID')



		user_name.send_keys('graeme')
		password = self.browser.find_element_by_id('id_password')
		self.assertEqual(password.get_attribute('placeholder'), 'Enter your password')
		password.send_keys('welcome1')
		password.send_keys(Keys.ENTER)
		self.assertIn('Sign on successful', self.browser.find_element_by_id('id_messages').text)

		# He goes to the Devices tab.

		# There is sees the list of registered devices.

		# On each device entry, it also shows its last message and when
		# it was sent.

		# There is also a search are where he can filter the device or 
		# devices shown.

		## ================================================================ ##
		#
		# Devices
		#	The registration and listing of the devices
		# Locations
		#	The list of location where the devices can be deployed.
		# Logs
		#	The data the comes from the devices - timesptamped
		# Units
		#	The units of data that is published by the devices
		#
		## ================================================================ ##

