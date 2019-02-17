from selenium import webdriver
import unittest

class newVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()



# Graeme comes to the PC and opesn the Leawood App by going to 
# http://host/leawood
	def test_can_see_the_dashboard(self):
		self.browser.get('http://localhost:8000')
		assert 'Leawood' in self.browser.title

		self.fail('Finish the test')

# He sees the amin menu. Since he is not signed in, there is only
# the option to sign in at the top.

# He also sees only the Dashboard that is in a read only mode.

# There is a search area where the devices can be searched for and
# the dashboard filtered for those/that specific device(s)

# The dashboard shows a graph for some of the devices.

# Graeme signs on and sees that the menu has expanded to be able 
# to manage the devices


# Devices
#	The registration and listing of the devices
# Locations
#	The list of location where the devices can be deployed.
# Logs
#	The data the comes from the devices - timesptamped
# Units
#	The units of data that is published by the devices


if __name__ == '__main__':
	unittest.main(warnings='ignore')

