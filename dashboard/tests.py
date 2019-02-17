from django.urls import resolve
from django.test import TestCase
from dashboard.views import dashboard
from django.http import HttpRequest

class SmokeTest(TestCase):

	def test_root_url_resolves_to_dashboard_view(self):
		found = resolve('/')
		self.assertEqual(found.func, dashboard)


	def test_dashboard_returns_correct_html(self):
		request = HttpRequest()
		response = dashboard(request)
		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>Leawood</title>', html)
		self.assertTrue(html.endswith('</html>'))