from django.urls import resolve
from django.test import TestCase
from devices.views import devices
from django.http import HttpRequest
from django.template.loader import render_to_string


class DevicesViewTest( TestCase ):
	def test_devices_resolves_to_devices_view(self):
		found = resolve('/devices/')
		self.assertEqual(found.func, devices)

	def test_devices_returns_correct_template(self):
		response = self.client.get('/devices/')
		# html = response.content.decode('utf8')
		# expected_html = render_to_string('dashboard/dashboard.html')
		# self.assertEqual(html, expected_html)
		self.assertTemplateUsed(response, 'devices/devices.html')
