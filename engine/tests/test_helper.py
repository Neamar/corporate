from engine.testcases import EngineTestCase
from engine import helper
from engine.models import Message,Player,Game
from website.models import User


class ModelTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def test_message_building_content(self):
		"""
		Check if the content is build properly
		"""
		g=Game(city="test_message_building",
			total_turn=10
			)
		g.save()
		u=User(username="lol",email="a@a.fr")
		u.save()
		p=Player(user=u,game=g)
		p.save()
		m=Message.objects.create(
			title="T1",
			content="C1",
			author=None,
			flag=Message.NOTE)
		m.save()
		m=Message.objects.create(
			title="T2",
			content="C3",
			author=None,
			flag=Message.NOTE)
		m.save()
		m=Message.objects.create(
			title="T1",
			content="C2",
			author=None,
			flag=Message.NOTE)
		m.save()


		opening="Opening"
		ending="Ending"
		m=helper.build_message_from_notes(
			message_type=Message.RESOLUTION,
			note_type=Message.NOTE,
			opening=opening,
			ending=ending,
			title="test",
			recipient_set=g.player_set.all()
			)
		expected_text="Opening\n## T1\n* C1\n* C2\n\n## T2\n* C3\nEnding"
		self.assertEquals(m.content,expected_text)

	def test_message_building_delivery(self):
		"""
		Check if messages are not misdelivered
		"""
		g=Game(city="test_message_building_2",
			total_turn=10
			)
		g.save()
		u1=User(username="lol1",email="a@a.fr")
		u1.save()
		p1=Player(user=u1,game=g)
		p1.save()
		u2=User(username="lol2",email="a@b.fr")
		u2.save()
		p2=Player(user=u2,game=g)
		p2.save()
		m=Message.objects.create(
			title="T1",
			content="C1",
			author=None,
			flag=Message.NOTE)
		m.save()
		m.recipient_set.add(p1)
		m=Message.objects.create(
			title="T2",
			content="C2",
			author=None,
			flag=Message.NOTE)
		m.save()
		m.recipient_set.add(p2)
		m=helper.build_message_from_notes(
			message_type=Message.RESOLUTION,
			note_type=Message.NOTE,
			title="test",
			To=[p2],
			recipient_set=p2
			)
		p2_only_receive_one_message=(Message.objects.filter(recipient_set=p2).count()==1)
		p2_reveive_message_T2=(Message.objects.filter(recipient_set=p2)[0].content=="T2")
		p1_receive_zero_message=(Message.objects.filter(recipient_set=p1).count()==0)
		validate_test=p2_only_receive_one_message and p2_reveive_message_T2 and p1_receive_zero_message

		self.assertEqual(validate_test, True)