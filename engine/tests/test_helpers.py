from engine.testcases import EngineTestCase
from engine import helpers
from engine.models import Message, Player


class ModelTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def test_message_building_content(self):
		"""
		Check if the content is built properly
		"""
		Message.objects.create(
			title="T1",
			content="C1",
			author=None,
			flag=Message.NOTE
		)
		Message.objects.create(
			title="T2",
			content="C3",
			author=None,
			flag=Message.NOTE
		)
		Message.objects.create(
			title="T1",
			content="C2",
			author=None,
			flag=Message.NOTE
		)

		opening="Opening"
		ending="Ending"
		m = helpers.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Message.objects.filter(flag=Message.NOTE),
			opening=opening,
			ending=ending,
			title="test",
		)

		expected = """Opening

## T1
* C1
* C2

## T2
* C3

Ending
"""
		self.assertEquals(m.content, expected)

	def test_notes_removed(self):
		"""
		Notes should be removed after aggregation
		"""
		# n2 has been removed
		Message.objects.create(
			title="T1",
			content="C1",
			author=None,
			flag=Message.NOTE
		)

		helpers.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Message.objects.filter(flag=Message.NOTE),
			title="test",
		)

		self.assertEqual(Message.objects.filter(flag=Message.NOTE).count(), 0)		
