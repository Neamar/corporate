from engine.testcases import EngineTestCase
from engine import helpers
from engine.models import Message,Player,Game
from website.models import User


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
		m=helpers.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Message.objects.filter(flag=Message.NOTE),
			opening=opening,
			ending=ending,
			title="test",
			recipient_set=self.g.player_set.all()
		)

		self.assertEquals(m.content,"Opening\n## T1\n* C1\n* C2\n\n## T2\n* C3\nEnding")

	def test_message_building_delivery(self):
		"""
		Check if messages are not misdelivered
		"""
		p2 = Player(game=self.g)
		p2.save()

		n1 = Message(
			title="T1",
			content="C1",
			author=None,
			flag=Message.NOTE
		)
		n1.save()
		n1.recipient_set.add(self.p)

		n2 = Message(
			title="T2",
			content="C2",
			author=None,
			flag=Message.NOTE
		)
		n2.save()
		n2.recipient_set.add(p2)

		helpers.build_message_from_notes(
			message_type=Message.RESOLUTION,
			notes=Message.objects.filter(flag=Message.NOTE,recipient_set=p2),
			title="test",
			recipient_set=[p2]
		)

		#p2_only receives one message
		self.assertEqual(Message.objects.filter(recipient_set=p2).count(), 1)
		#p2 receive message T2
		self.assertEqual(Message.objects.filter(recipient_set=p2)[0].content, "\n## T2\n* C2\n")
		#p1 receive no message
		self.assertEqual(Message.objects.filter(recipient_set=self.p).exclude(flag=Message.NOTE).count(), 0)
