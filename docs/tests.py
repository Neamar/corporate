from django.test import TestCase, Client


class DocTest(TestCase):
	def setUp(self):
		self.c = Client()

	def test_doc_is_available(self):
		"""
		Check existing pages are served
		"""

		r = self.c.get('/docs/index')
		self.assertEqual(r.status_code, 200)
		self.assertTemplateUsed('/docs/index.html')

	def test_doc_markdown(self):
		"""
		Unknown page returns 404
		"""

		r = self.c.get('/docs/index')
		self.assertIn('<p>', r.content)

	def test_doc_index(self):
		"""
		Index is served by default
		"""

		r = self.c.get('/docs/')
		self.assertEqual(r.status_code, 200)
		self.assertTemplateUsed('/docs/index.html')

	def test_doc_dotted(self):
		"""
		Dotted path are forbidden
		"""

		r = self.c.get('/docs/../views.py')
		self.assertEqual(r.status_code, 404)
		self.assertTemplateNotUsed('/docs/index.html')

	def test_doc_unknown_page(self):
		"""
		Unknown page returns 404
		"""

		r = self.c.get('/docs/hello-not-here')
		self.assertEqual(r.status_code, 404)
		self.assertTemplateNotUsed('/docs/index.html')

	def test_doc_corporation(self):
		"""
		Corporation should be served
		"""

		r = self.c.get('/docs/corporations/c')
		self.assertEqual(r.status_code, 200)
		self.assertTemplateUsed('/docs/corporation.html')

	def test_doc_unknown_corporation(self):
		"""
		Corporation should be 404 when not existing
		"""

		r = self.c.get('/docs/corporations/arespublica')
		self.assertEqual(r.status_code, 404)
		self.assertTemplateNotUsed('/docs/corporation.html')
