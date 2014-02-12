from engine.models import Player
from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.share.models import Share
from engine_modules.mdc.models import MDCVoteOrder, MDCVoteSession
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder, DerivativeSpeculationOrder

from engine_modules.mdc.tasks import MDCLineCPUBTask

class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.p2 = Player(game=self.g)
		self.p2.save()

		self.p3 = Player(game=self.g)
		self.p3.save()

		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.c)
		self.c2 = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c2)
		self.c3 = Corporation(base_corporation_slug='ares', assets=10)
		self.g.corporation_set.add(self.c3)

		self.s = Share(
			corporation=self.c,
			player=self.p,
			turn=self.g.current_turn
		)
		self.s.save()

		self.s2 = Share(
			corporation=self.c2,
			player=self.p2,
			turn=self.g.current_turn
		)
		self.s2.save()

		self.s3 = Share(
			corporation=self.c3,
			player=self.p3,
			turn=self.g.current_turn
		)
		self.s3.save()

		self.v = MDCVoteOrder(
			player=self.p,
			party_line=MDCVoteOrder.DERE
		)
		self.v.save()

		self.v2 = MDCVoteOrder(
			player=self.p2,
			party_line=MDCVoteOrder.CPUB
		)
		self.v2.save()

		self.v3 = MDCVoteOrder(
			player=self.p3,
			party_line=MDCVoteOrder.DEVE
		)
		self.v3.save()

		self.g.disable_invisible_hand = True
		self.g.save()


	def test_MDC_CPUB_line_effects(self):
		"""
		Test what happens when the CPUB party line is chosen
		"""

		initial_assets = self.c.assets
		initial_assets2 = self.c2.assets
		initial_assets3 = self.c3.assets
		
		self.v.party_line = MDCVoteOrder.CPUB
		self.v.save()

		self.v2.party_line = MDCVoteOrder.CPUB
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.DEVE
		self.v3.save()

		self.g.resolve_current_turn()

		# We have to resolve twice: once for the MDCVoteOrders to be taken into account
		# And once for the resulting MDCVoteSession to be effective
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, initial_assets + 1)
		self.assertEqual(self.reload(self.c2).assets, initial_assets2 + 1)
		self.assertEqual(self.reload(self.c3).assets, initial_assets3 - 1)

	def test_MDC_DEVE_line_effects(self):
		"""
		Test what happens when the CPUB party line is chosen
		"""

		initial_assets = self.c.assets
		initial_assets2 = self.c2.assets
		initial_assets3 = self.c3.assets
		
		self.v.party_line = MDCVoteOrder.CPUB
		self.v.save()

		self.v2.party_line = MDCVoteOrder.DEVE
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.DEVE
		self.v3.save()

		self.g.resolve_current_turn()

		# We have to resolve twice: once for the MDCVoteOrders to be taken into account
		# And once for the resulting MDCVoteSession to be effective
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, initial_assets - 1)
		self.assertEqual(self.reload(self.c2).assets, initial_assets2 + 1)
		self.assertEqual(self.reload(self.c3).assets, initial_assets3 + 1)

	def test_MDC_CCIB_line_effects(self):
		"""
		Test what happens when the CCIB party line is chose
		"""

		self.v.party_line = MDCVoteOrder.CCIB
		self.v.save()

		self.v2.party_line = MDCVoteOrder.CCIB
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.TRAN
		self.v3.save()

		self.g.resolve_current_turn()

		# We have to resolve twice: once for the MDCVoteOrders to be taken into account
		# And once for the resulting MDCVoteSession to be effective
		self.g.resolve_current_turn()

	def test_MDC_TRAN_line_effects(self):
		"""
		Test what happens when the CCIB party line is chose
		"""

		self.v.party_line = MDCVoteOrder.CCIB
		self.v.save()

		self.v2.party_line = MDCVoteOrder.TRAN
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.TRAN
		self.v3.save()

		self.g.resolve_current_turn()

		# We have to resolve twice: once for the MDCVoteOrders to be taken into account
		# And once for the resulting MDCVoteSession to be effective
		self.g.resolve_current_turn()

	def test_MDC_BANK_line_negative_effect(self):
		"""
		Test what happens when the BANK party line is chose
		"""

		self.v.party_line = MDCVoteOrder.BANK
		self.v.save()

		self.v2.party_line = MDCVoteOrder.BANK
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.DERE
		self.v3.save()

		self.g.resolve_current_turn()

		# Player 3 has voted Deregulation, so he shouldn't be able to speculate
		d = Derivative(name="first and last")
		d.save()
		d.corporations.add(self.c, self.c2)

		o = CorporationSpeculationOrder(
			player=self.p3,
			corporation=self.c3,
			rank=1,
			investment=1
		)
		self.assertRaises(OrderNotAvailable, o.clean)

		# Check that player 1 still can
		o2 = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.c3,
			rank=1,
			investment=1
		)
		o2.clean()

		dso = DerivativeSpeculationOrder(
                        player=self.p3,
                        speculation=DerivativeSpeculationOrder.UP,
                        investment=DerivativeSpeculationOrder.MAX_AMOUNT_SPECULATION - 1
                )
                self.assertRaises(OrderNotAvailable, dso.clean)

		dso2 = DerivativeSpeculationOrder(
                        player=self.p,
                        speculation=DerivativeSpeculationOrder.UP,
                        investment=DerivativeSpeculationOrder.MAX_AMOUNT_SPECULATION - 1
                )
		dso2.clean()

	def test_MDC_DERE_line_negative_effect(self):
		"""
		Test what happens when the BANK party line is chose
		"""

		self.v.party_line = MDCVoteOrder.BANK
		self.v.save()

		self.v2.party_line = MDCVoteOrder.DERE
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.DERE
		self.v3.save()

		self.g.resolve_current_turn()

		# Player 1 has voted Garde Fous Bancaires, so he shouldn't be able to speculate
		d = Derivative(name="first and last")
		d.save()
		d.corporations.add(self.c, self.c2)

		o = CorporationSpeculationOrder(
			player=self.p,
			corporation=self.c3,
			rank=1,
			investment=5
		)
		self.assertRaises(OrderNotAvailable, o.clean)

		dso = DerivativeSpeculationOrder(
                        player=self.p,
                        speculation=DerivativeSpeculationOrder.UP,
                        investment=DerivativeSpeculationOrder.MAX_AMOUNT_SPECULATION - 1
                )
                self.assertRaises(OrderNotAvailable, dso.clean)

		# Check that player 3 still can
		o2 = CorporationSpeculationOrder(
			player=self.p3,
			corporation=self.c3,
			rank=1,
			investment=5
		)
		o2.clean()

		dso2 = DerivativeSpeculationOrder(
                        player=self.p3,
                        speculation=DerivativeSpeculationOrder.UP,
                        investment=DerivativeSpeculationOrder.MAX_AMOUNT_SPECULATION - 1
                )
		dso2.clean()
