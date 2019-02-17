from selenium import webdriver
import unittest

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

		self.fail('Finish the test')

		# He sees the main menu bar. Since he is not signed in, there is only
		# the dashboard tab and an option to sign in at the top.

		# He also sees only the Dashboard that is in a view only mode.

		# The dashboard shows a graph for some of the devices.

		# There is a search area where the devices can be searched for and
		# the dashboard filtered for those/that specific device(s)

		# Graeme signs on and sees that the menu has expanded to be able 
		# to manage the devices

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


if __name__ == '__main__':
	unittest.main(warnings='ignore')

