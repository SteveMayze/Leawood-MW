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

class FunctionalTest(LiveServerTestCase):

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

