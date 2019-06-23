from django.urls import resolve
from django.test import TestCase
from devices.views import devices
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render
from devices.models import Device
from unittest.mock import patch, Mock
import unittest
from django.test import Client
from dashboard.tests import common


class ActiveDevicesViewRenderTest( TestCase ):
	def setUp(self):
		self.request = HttpRequest()
		self.context = {}
		self.context["current_tab"] = "active"

	def test_devices_resolves_to_devices_view(self):
		found = resolve('/devices/')
		self.assertEqual(found.func, devices)

	def test_active_contains_only_active_devices( self ):
		context_dict = self.context

		common.create_sample_data()

		context_dict["active_objects"] = Device.objects.filter(registered = True )
		response = render(self.request, 'devices/devices.html', context=context_dict)
		self.assertNotContains(response, 'pending item 1')
		self.assertNotContains(response, 'pending item 2')
		self.assertContains(response, 'active item 2')
		self.assertContains(response, 'active item 2')

	def test_pagination( self ):
		common.create_random_data(20)
		context_dict = self.context
		response = self.client.get('/devices/')
		self.assertContains(response, "1 of 2")

	def test_pagination_has_query_set( self ):
		common.create_random_data(20)
		context_dict = self.context
		response = self.client.get('/devices/')

		self.assertContains(response, "1 of 2")

	def test_pagination_navigate_to_page_2( self ):
		common.create_random_data(20)
		context_dict = self.context
		response = self.client.get('/devices/?p=2')

		self.assertContains(response, "2 of 2")

class ActiveDevicesViewTest( TestCase ):
	def setUp(self):
		self.request = HttpRequest()
		self.context = {}
		self.context["current_tab"] = "active"

	def test_devices_resolves_to_devices_view(self):
		response = self.client.get('/devices/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "devices/active.html")

	def test_default_tab_is_devices( self ):
		response = self.client.get('/devices/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['current_tab'], 'active')



# Although this is a tab, for the purpose of testing, this will 
# try to be treated as a view.
class PendingDevicesViewRenderTest( TestCase ):

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

		common.create_sample_data()

		context_dict["pending_objects"] = Device.objects.filter(registered = False )
		response = render(self.request, 'devices/devices.html', context=context_dict)
		self.assertContains(response, 'pending item 1')
		self.assertContains(response, 'pending item 2')
		self.assertNotContains(response, 'active item 1')
		self.assertNotContains(response, 'active item 2')



class PendingDevicesViewTest( TestCase ):

	def setUp(self):

		self.client = Client()

		self.request = HttpRequest()
		self.context = {}
		self.context["current_tab"] = "pending"

	def test_that_pending_context_opens_pending_tab( self ):
		response = self.client.get('/devices/', {
			'pagename':'Devices', 'current_tab': 'pending'}
			)

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "devices/pending.html")

	def test_pending_contains_only_pending_devices( self ):

		common.create_sample_data()

		context_dict = self.context
		context_dict['pending_objects'] = Device.objects.filter(registered = False )
		context_dict['pagename'] = 'Devices'

		response = self.client.get('/devices/', context_dict)


		self.assertEqual(response.status_code, 200)

		self.assertContains(response, 'pending item 1')
		self.assertContains(response, 'pending item 2')

