from .base import FunctionalTest, TEST_EMAIL
from selenium.webdriver.common.keys import Keys
import time


class DashboardTest(FunctionalTest):

	def test_can_see_the_dashboard(self):
		# Graeme comes to the PC and opens the Leawood App by going to 
		# http://host/leawood

		self.browser.get(self.live_server_url)
		assert 'Leawood' in self.browser.title
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
		test_user = self.create_user('graeme', 'welcome1', TEST_EMAIL)

		self.browser.get(self.live_server_url)

		signin_link = self.browser.find_element_by_link_text('Sign in')
		signin_link.click()

		login_dialog = self.browser.find_element_by_id('id_loginModal')
		self.assertIn('show', login_dialog.get_attribute('class'))

		user_name = self.browser.find_element_by_id('id_login_username')

		user_name.send_keys('graeme')
		password = self.browser.find_element_by_id('id_login_password')
		password.send_keys('welcome1')
		password.send_keys(Keys.ENTER)
		self.wait_for_link('Sign off')
		self.assertIn('Login was successful.', self.browser.find_elements_by_class_name('messages')[0].text)


		# He goes to the Devices tab.
		devices_link = self.browser.find_element_by_link_text('Devices')
		devices_link.click()

		# There is sees the list of registered devices.
		self.wait_for( self.browser.find_element_by_id('id_device_list') )

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

