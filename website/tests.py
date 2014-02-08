from django.test import Client
from django.core.urlresolvers import reverse

from engine.testcases import EngineTestCase


class WebsiteTest(EngineTestCase):
	def setUp(self):
		self.client = Client()
		super(WebsiteTest, self).setUp()


class OrderWebsiteTest(WebsiteTest):
	def test_orders_require_login(self):
		r = self.client.get(reverse('website.views.orders', args=[self.g.id]))
		self.assertEqual(r.status_code, 302)

	def test_posting_orders_require_login(self):
		r = self.client.get(reverse('website.views.add_order', args=[self.g.id, 'BuyInfluenceOrder']))
		self.assertEqual(r.status_code, 302)

	def test_posting_orders_require_valid_order(self):
		pass
