from django.test import Client
from django.core.urlresolvers import reverse

from engine.testcases import EngineTestCase
from website.models import User


class WebsiteTest(EngineTestCase):
	def setUp(self):
		super(WebsiteTest, self).setUp()

		password = "password"
		self.u = User(username="hello")
		self.u.set_password(password)
		self.u.save()

		self.p.user = self.u
		self.p.save()

		self.client = Client()

		self.authenticated_client = Client()
		is_logged_in = self.authenticated_client.login(username=self.u.username, password=password)
		self.assertTrue(is_logged_in)

	def test_index_and_admin_up_nologin(self):
		"""
		Checking index also checks admin forms are properly configured
		"""

		pages = [
			'website.views.index.index',
			'django.contrib.auth.views.login',
			'admin:index',
		]

		for page in pages:
			r = self.client.get(reverse(page))
			self.assertEqual(r.status_code, 200)

	def test_pages_require_login(self):
		pages = [
			reverse('website.views.orders.orders', args=[self.g.id]),
			reverse('website.views.orders.add_order', args=[self.g.id, 'BuyInfluenceOrder']),
			reverse('website.views.orders.delete_order', args=[self.g.id, 1]),
			reverse('website.views.datas.wallstreet', args=[self.g.id]),
			reverse('website.views.datas.corporations', args=[self.g.id]),
			reverse('website.views.datas.players', args=[self.g.id]),
		]

		for page in pages:
			r = self.client.get(page)
			self.assertEqual(r.status_code, 302)

	def test_pages_up(self):
		pages = [
			reverse('website.views.orders.orders', args=[self.g.id]),
			reverse('website.views.orders.add_order', args=[self.g.id, 'BuyInfluenceOrder']),
			reverse('website.views.datas.wallstreet', args=[self.g.id]),
			reverse('website.views.datas.corporations', args=[self.g.id]),
			reverse('website.views.datas.corporation', args=[self.g.id, self.c.base_corporation_slug]),
			reverse('website.views.datas.players', args=[self.g.id]),
			reverse('website.views.datas.player', args=[self.g.id, self.p.id]),
		]

		for page in pages:
			r = self.authenticated_client.get(page)
			self.assertEqual(r.status_code, 200)

	def test_pages_redirect(self):
		from engine_modules.influence.models import BuyInfluenceOrder
		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()

		pages = [
			reverse('website.views.orders.delete_order', args=[self.g.id, 1]),
		]

		for page in pages:
			r = self.authenticated_client.get(page)
			self.assertEqual(r.status_code, 302)
