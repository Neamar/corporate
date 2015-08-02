from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class CommandsTest(TestCase):
	def test_stubgame(self):
		out = StringIO()
		call_command('stubgame', stdout=out)
		self.assertIn('Created game #', out.getvalue())

	def test_advancedstubgame(self):
		out = StringIO()
		call_command('advancedstubgame', stdout=out)
		self.assertIn('Simulated turn #', out.getvalue())
