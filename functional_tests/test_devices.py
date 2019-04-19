from .base import FunctionalTest, TEST_EMAIL
from selenium.webdriver.common.keys import Keys
import time



class DevicesTest(FunctionalTest):

	def test_can_see_the_front_page(self):
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
		self.wait_for(lambda: self.browser.find_element_by_id('id_device_list') )

		# At the start, there would be no devices. There needs to be a means
		# to register a device.

