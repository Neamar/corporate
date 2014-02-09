from django.test import Client
from django.core.urlresolvers import reverse

from engine.testcases import EngineTestCase
from website.models import User


class WebsiteTest(EngineTestCase):
	def setUp(self):
		self.u = User(username="hello")
		self.u.set_password("password")
		self.u.save()

		self.client = Client()

		self.authenticated_client = Client()
		self.authenticated_client.login(username=self.u.username, password='password')
		super(WebsiteTest, self).setUp()

	def test_pages_require_login(self):
		pages = [
			'website.views.orders',
			'website.views.wallstreet',
			'website.views.corporations',
			'website.views.players',
		]

		for page in pages:
			r = self.client.get(reverse(page, args=[self.g.id]))
			self.assertEqual(r.status_code, 302)

	def test_posting_orders_require_login(self):
		r = self.client.get(reverse('website.views.add_order', args=[self.g.id, 'BuyInfluenceOrder']))
		self.assertEqual(r.status_code, 302)

	def test_wallstreet(self):
		r = self.authenticated_client.get(reverse('website.views.wallstreet', args=[self.g.id]))
		self.assertEqual(r.status_code, 200)
	
	def test_corporations(self):
		r = self.authenticated_client.get(reverse('website.views.corporations', args=[self.g.id]))
		self.assertEqual(r.status_code, 200)

	def test_players(self):
		r = self.authenticated_client.get(reverse('website.views.players', args=[self.g.id]))
		self.assertEqual(r.status_code, 200)
