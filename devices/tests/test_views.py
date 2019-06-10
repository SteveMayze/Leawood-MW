from django.urls import resolve
from django.test import TestCase
from devices.views import devices
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render
from devices.models import Device

def create_sample_data():
	device = Device.objects.create(
		name = "active item 1", 
		serial_id='123',
		description="active item description", 
		address='ABC',
		registered=True
		)

	device = Device.objects.create(
		name = "active item 2", 
		serial_id='234',
		description="active item description", 
		address='DEF',
		registered=True
		)

	device = Device.objects.create(
		name = "pending item 1", 
		serial_id='345',
		description="pending item description", 
		address='GHI',
		registered=False
		)

	device = Device.objects.create(
		name = "pending item 2", 
		serial_id='456',
		description="pending item description", 
		address='JKL',
		registered=False
		)


class ActiveDevicesViewTest( TestCase ):
	def setUp(self):
		self.request = HttpRequest()
		self.context = {}
		self.context["current_tab"] = "active"

	def test_devices_resolves_to_devices_view(self):
		found = resolve('/devices/')
		self.assertEqual(found.func, devices)

	def test_devices_returns_correct_template(self):
		response = self.client.get('/devices/')
		self.assertTemplateUsed(response, 'devices/devices.html')

	def test_default_tab_is_devices( self ):
		response = self.client.get('/devices/')
		self.assertEqual(response.context['current_tab'], 'active')

	def test_active_contains_only_active_devices( self ):
		context_dict = self.context

		create_sample_data()

		context_dict["active_objects"] = Device.objects.filter(registered = True )
		response = render(self.request, 'devices/devices.html', context=context_dict)
		self.assertNotContains(response, 'pending item 1')
		self.assertNotContains(response, 'pending item 2')
		self.assertContains(response, 'active item 2')
		self.assertContains(response, 'active item 2')



# Although this is a tab, for the purpose of testing, this will 
# try to be treaded as a view.
class PendingDevicesViewTest( TestCase ):
	def setUp(self):
		self.request = HttpRequest()
		self.context = {}
		self.context["current_tab"] = "pending"

	def test_that_pending_context_opens_pending_tab( self ):
		context_dict = self.context
		response = render(self.request, 'devices/devices.html', context=context_dict)
		self.assertContains(response, "<h1>Pending</h1>")

	def test_pending_contains_only_pending_devices( self ):
		context_dict = self.context

		create_sample_data()

		context_dict["pending_objects"] = Device.objects.filter(registered = False )
		response = render(self.request, 'devices/devices.html', context=context_dict)
		self.assertContains(response, 'pending item 1')
		self.assertContains(response, 'pending item 2')
		self.assertNotContains(response, 'active item 2')
		self.assertNotContains(response, 'active item 2')


