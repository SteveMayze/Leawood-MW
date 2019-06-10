from .base import FunctionalTest, TEST_EMAIL
from selenium.webdriver.common.keys import Keys
import time



class DevicesTest(FunctionalTest):

	def test_can_see_the_front_page(self):
		# Graeme signs on and sees that the menu has expanded to be able 
		# to manage the devices
		test_user = self.create_user('graeme', 'welcome1', TEST_EMAIL)
		# session_key = create_pre_authenticated_session('graeme')
		# self.browser.get(self.live_server_url + "/404_no_such_url")
		# self.browser.add_cookie(dict(
		# 	name=settings.SESSION_COOKIE_NAME,
		# 	value=session_key,
		# 	path='/'
		# ))		

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

		# Initially, there are no devices registered. They have to be paired. 
		# So there should be just an empty list
		self.wait_for(lambda: self.browser.find_element_by_id('id_active_list') )

		# The page has a an empty list of devices. There are two tabs. One for 
		# Devices (the default) and one for Pending devices and registration of new ones. 
		# The Devices tab is empty. There is only a search form and an empty list.

		self.browser.find_element_by_link_text('Active')
		searchbox = self.browser.find_element_by_id('id_search_filter')
		self.assertEqual(searchbox.get_attribute('placeholder'), 'device filter')

		# Since this page is empty, Graeme clicks on the "Pending" tab to see what is there.

		self.browser.find_element_by_link_text('Pending').click()
		# On the Pending page, there is also a list and also empty - with a search bar. 
		# There are two buttones. One to register a device manually and another to scan for 
		# any new devices in the area.
		searchbox = self.browser.find_element_by_id('id_search_filter')
		self.assertEqual(searchbox.get_attribute('placeholder'), 'device filter')



		# SCANNING FOR A DEVICE
		# =====================

		# Once the scan is initiated, the page counts down from 60 As the page counts 
		# down, it will be updated with the devices that are found. 
		# In essence, the scan will broadcast a message to invite any device, not
		# yet paired to introduce them selves.
		# These are then populated to a able on the "paring page"
		# Graeme can click on the device name and view its properties and allocate
		# a location
		# From the summary page, it is possible to click the check boxes and mark the
		# selected devices as registered.


		# The device itself will not be considered registered until the full process
		# has been completed. ie once marked as registered, a message is sent to the 
		# device record the Home Base and not longer accept scan requests.

		# The device can be de-registered in which case the device will be released
		# If there are problems with this process, the device can be set back to 
		# Factory Settings at the device itself. 


