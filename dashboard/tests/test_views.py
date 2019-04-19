from django.urls import resolve
from django.test import TestCase
from dashboard.views import dashboard
from django.http import HttpRequest
from django.template.loader import render_to_string

class DashboardViewTest(TestCase):

	def test_root_url_resolves_to_dashboard_view(self):
		found = resolve('/')
		self.assertEqual(found.func, dashboard)

	def test_leawood_url_resolves_to_dashboard_view(self):
		found = resolve('/leawood/')
		self.assertEqual(found.func, dashboard)


	def test_dashboard_returns_correct_html(self):
		response = self.client.get('/')
		# html = response.content.decode('utf8')
		# expected_html = render_to_string('dashboard/dashboard.html')
		# self.assertEqual(html, expected_html)
		self.assertTemplateUsed(response, 'dashboard/dashboard.html')


