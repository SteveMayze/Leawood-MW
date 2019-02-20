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

	def wait_for_modal_close(self, modal_id):
		start_time = time.time()
		while True:
			try:
				model = self.browser.find_element_by_id(modal_id)
				self.assertNotIn('show', model.get_attribute('class'))
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def wait_for_modal_show(self, modal_id):
		start_time = time.time()
		while True:
			try:
				model = self.browser.find_element_by_id(modal_id)
				self.assertIn('show', model.get_attribute('class'))
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def check_placeholder(self, element_id, value):
		element = self.browser.find_element_by_id(element_id)
		self.assertEqual(element.get_attribute('placeholder'), value)

