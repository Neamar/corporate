# -*- coding: utf-8 -*-
from django.test.utils import override_settings
from django.test import Client
from django.core.urlresolvers import reverse

from messaging.models import Message
from engine.testcases import EngineTestCase
from website.models import User


@override_settings(PASSWORD_HASHERS=('django.contrib.auth.hashers.SHA1PasswordHasher',))
class ViewsTest(EngineTestCase):
	def setUp(self):
		super(ViewsTest, self).setUp()

		password = "password"
		self.u = User(username="hello")
		self.u.set_password(password)
		self.u.save()

		self.p.user = self.u
		self.p.save()
		m = Message.objects.create(
			author=None,
			title="test",
			content="hi",
			turn=self.g.current_turn
		)
		m.recipient_set.add(self.p)

		self.client = Client()

		self.authenticated_client = Client()
		is_logged_in = self.authenticated_client.login(username=self.u.username, password=password)
		self.assertTrue(is_logged_in)

	def test_pages_up_nologin(self):
		"""
		Checking admin:index also checks admin forms are properly configured
		"""

		pages = [
			'website.views.index.index',
			'django.contrib.auth.views.login',
			'website.views.index.signup',
		]

		for page in pages:
			r = self.client.get(reverse(page))
			self.assertEqual(r.status_code, 200)

	def test_pages_require_login(self):
		"""
		Check pages can't be seen without being logged
		"""
		pages = [
			reverse('website.views.orders.orders', args=[self.g.id]),
			reverse('website.views.orders.add_order', args=[self.g.id, 'BuyInfluenceOrder']),
			reverse('website.views.orders.delete_order', args=[self.g.id, 1]),
			reverse('website.views.data.wallstreet', args=[self.g.id]),
			reverse('website.views.data.wallstreet', args=[self.g.id, self.g.current_turn - 1]),
			reverse('website.views.data.corporations', args=[self.g.id]),
			reverse('website.views.data.players', args=[self.g.id]),
			reverse('website.views.data.shares', args=[self.g.id]),
			reverse('website.views.data.shares', args=[self.g.id, self.g.current_turn - 1]),
			reverse('website.views.data.newsfeeds', args=[self.g.id]),
			reverse('website.views.data.newsfeeds', args=[self.g.id, self.g.current_turn - 1]),
			reverse('website.views.data.comlink', args=[self.g.id]),
			reverse('website.views.data.message', args=[self.g.id, self.p.message_set.get().pk]),
		]

		for page in pages:
			r = self.client.get(page)
			self.assertEqual(r.status_code, 302)

	def test_pages_up(self):
		"""
		Check pages return with 200 status code
		"""
		pages = [
			reverse('website.views.orders.orders', args=[self.g.id]),
			reverse('website.views.orders.add_order', args=[self.g.id, 'BuyInfluenceOrder']),
			reverse('website.views.data.wallstreet', args=[self.g.id]),
			reverse('website.views.data.wallstreet', args=[self.g.id, self.g.current_turn - 1]),
			reverse('website.views.data.corporations', args=[self.g.id]),
			reverse('website.views.data.corporation', args=[self.g.id, self.c.base_corporation_slug]),
			reverse('website.views.data.players', args=[self.g.id]),
			reverse('website.views.data.player', args=[self.g.id, self.p.id]),
			reverse('website.views.data.shares', args=[self.g.id]),
			reverse('website.views.data.shares', args=[self.g.id, self.g.current_turn - 1]),
			reverse('website.views.data.newsfeeds', args=[self.g.id]),
			reverse('website.views.data.newsfeeds', args=[self.g.id, self.g.current_turn - 1]),
			reverse('website.views.data.comlink', args=[self.g.id]),
			reverse('website.views.data.message', args=[self.g.id, self.p.message_set.get().pk]),
		]

		for page in pages:
			r = self.authenticated_client.get(page)
			self.assertEqual(r.status_code, 200)

	def test_pages_redirect(self):
		"""
		Check pages redirect after use
		"""
		from engine_modules.influence.models import BuyInfluenceOrder
		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()

		pages = [
			reverse('website.views.orders.delete_order', args=[self.g.id, o.pk]),
		]

		for page in pages:
			r = self.authenticated_client.get(page)
			self.assertEqual(r.status_code, 302)

	def test_pages_down(self):
		"""
		Check invalid page render 404
		"""
		pages = [
			reverse('website.views.data.newsfeeds', args=[self.g.id, self.g.current_turn + 1]),
			reverse('website.views.data.wallstreet', args=[self.g.id, self.g.current_turn + 1]),
		]

		for page in pages:
			r = self.authenticated_client.get(page)
			self.assertEqual(r.status_code, 404)

	def test_post_order(self):
		"""
		Check we can create an order
		"""

		from engine_modules.influence.models import BuyInfluenceOrder

		page = reverse('website.views.orders.add_order', args=[self.g.id, 'BuyInfluenceOrder'])
		r = self.authenticated_client.post(page)

		# We're redirected
		self.assertEqual(r.status_code, 302)

		# An order was created
		o = BuyInfluenceOrder.objects.get()
		self.assertEqual(self.p, o.player)

	def test_orders_page(self):
		"""
		Check orders page display current orders
		"""
		from engine_modules.influence.models import BuyInfluenceOrder
		o = BuyInfluenceOrder(
			player=self.p
		)
		o.save()

		# Order is displayed
		page = reverse('website.views.orders.orders', args=[self.g.id])
		r = self.authenticated_client.post(page)
		self.assertIn(o, r.context['existing_orders'])
