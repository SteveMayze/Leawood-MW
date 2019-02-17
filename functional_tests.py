from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class newVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()



	def test_can_see_the_dashboard(self):
		# Graeme comes to the PC and opens the Leawood App by going to 
		# http://host/leawood
		self.browser.get('http://localhost:8000')
		assert 'Leawood' in self.browser.title


		# He sees the main menu bar. Since he is not signed in, there is only
		# the dashboard tab and an option to sign in at the top.
		# TODO

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

		device_table self.browser.find_element_by_id('id_device_table')
		rows = device_table.find_elements_by_tag_name('tr')
		self.assertTrue(
			all('solar' in row.text)
		)



		# Graeme signs on and sees that the menu has expanded to be able 
		# to manage the devices

		# He goes to the Devices tab.

		# There is sees the list of registered devices.

		# On each device entry, it also shows its last message and when
		# it was sent.

		# There is also a search are where he can filter the device or 
		# devices shown.

		self.fail('Finish the test')

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


if __name__ == '__main__':
	unittest.main(warnings='ignore')

