from django.urls import resolve
from django.test import TestCase
from devices.views import devices, pairing
from django.http import HttpRequest
from django.template.loader import render_to_string


class DevicesViewTest( TestCase ):
	def test_devices_resolves_to_devices_view(self):
		found = resolve('/devices/')
		self.assertEqual(found.func, devices)

	def test_devices_returns_correct_template(self):
		response = self.client.get('/devices/')
		self.assertTemplateUsed(response, 'devices/devices.html')



class PairingViewTest( TestCase ):
	def test_pairing_resolves_to_pairing_view( self ):
		found = resolve('/devices/pairing')
		self.assertEqual(found.func, pairing )

	def test_pairing_returns_correct_template(self):
		response = self.client.get('/devices/pairing')
		self.assertTemplateUsed(response, 'devices/pairing.html')


