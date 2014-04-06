from engine.testcases import EngineTestCase


class SignalsTest(EngineTestCase):
	def test_derivatives_created(self):
		nikkei = self.g.derivative_set.get(name="Nikkei")
		self.assertIn(self.c, nikkei.corporations.all())
