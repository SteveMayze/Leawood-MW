from django.urls import resolve
from django.test import TestCase
from dashboard.views import dashboard

class SmokeTest(TestCase):

	def test_root_url_resolves_to_dashboard_view(self):
		found = resolve('/')
		self.assertEqual(found.func, dashboard)