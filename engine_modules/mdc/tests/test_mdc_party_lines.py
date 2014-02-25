from engine.models import Player
from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.share.models import Share
from engine_modules.mdc.models import MDCVoteOrder, MDCVoteSession
from engine_modules.corporation.models import Corporation
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder, DerivativeSpeculationOrder
from engine_modules.corporation_run.models import ProtectionOrder, DataStealOrder, SabotageOrder, ExtractionOrder

from engine_modules.mdc.tasks import MDCLineCPUBTask

class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.p2 = Player(game=self.g)
		self.p2.save()

		self.p3 = Player(game=self.g)
		self.p3.save()

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

	def set_Turn_Line(self, L1, L2, L3):
		"""
		A little helper to set the Line each player has voted for this turn
		"""

		self.v.party_line = L1
		self.v.save()

		self.v2.party_line = L2
		self.v2.save()

		self.v3.party_line = L3
		self.v3.save()


	def test_MDC_CPUB_line_effects(self):
		"""
		Test what happens when the CPUB party line is chosen
		"""

		initial_assets = self.c.assets
		initial_assets2 = self.c2.assets
		initial_assets3 = self.c3.assets

		self.set_Turn_Line(MDCVoteOrder.CPUB, MDCVoteOrder.CPUB, MDCVoteOrder.DEVE)
		
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
		
		self.set_Turn_Line(MDCVoteOrder.CPUB, MDCVoteOrder.DEVE, MDCVoteOrder.DEVE)

		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, initial_assets - 1)
		self.assertEqual(self.reload(self.c2).assets, initial_assets2 + 1)
		self.assertEqual(self.reload(self.c3).assets, initial_assets3 + 1)

	def test_MDC_CCIB_line_positive_effects(self):
		"""
		Test what happens to voters of the CCIB party line when it is chosen
		"""

		self.set_Turn_Line(MDCVoteOrder.CCIB, MDCVoteOrder.CCIB, MDCVoteOrder.TRAN)
		self.g.resolve_current_turn()

		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=5,
		)
		dso.clean()
		dso.save()

		so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			additional_percents=5,
		)
		so.clean()
		so.save()

		eo = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			kidnapper_corporation=self.c2
		)
		eo.clean()
		eo.save()

		self.assertEqual(dso.get_raw_probability(), dso.additional_percents * 10 + dso.PROBA_SUCCESS - 10)
		self.assertEqual(so.get_raw_probability(), so.additional_percents * 10 + so.PROBA_SUCCESS - 10)
		self.assertEqual(eo.get_raw_probability(), eo.additional_percents * 10 + eo.PROBA_SUCCESS - 10)

	def test_MDC_CCIB_line_negative_effects(self):
		"""
		Test what happens when the CCIB party line is chosen to players who voted for transparency
		"""

		self.set_Turn_Line(MDCVoteOrder.CCIB, MDCVoteOrder.CCIB, MDCVoteOrder.TRAN)
		self.g.resolve_current_turn()

		# Player 3 has voted transparency, so he should'nt be able to have a protection run
		po = ProtectionOrder(
                        player=self.p3,
                        protected_corporation=self.c,
                        defense=ProtectionOrder.SABOTAGE,
                )
		self.assertRaises(OrderNotAvailable, po.clean)

		# Check that player 1 stil can
		po2 = ProtectionOrder(
                        player=self.p,
                        protected_corporation=self.c,
                        defense=ProtectionOrder.SABOTAGE,
                )
		po2.clean()

	def test_MDC_TRAN_line_effects(self):
		"""
		Test what happens when the TRAN party line is chosen
		"""

		self.set_Turn_Line(MDCVoteOrder.CCIB, MDCVoteOrder.TRAN, MDCVoteOrder.TRAN)
		self.g.resolve_current_turn()

		dso = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p,
			target_corporation=self.c,
			additional_percents=5,
		)
		dso.clean()
		dso.save()

		so = SabotageOrder(
			player=self.p,
			target_corporation=self.c,
			additional_percents=5,
		)
		so.clean()
		so.save()

		eo = ExtractionOrder(
			player=self.p,
			target_corporation=self.c,
			kidnapper_corporation=self.c2
		)
		eo.clean()
		eo.save()

		self.assertEqual(dso.get_raw_probability(), dso.additional_percents * 10 + dso.PROBA_SUCCESS - 10)
		self.assertEqual(so.get_raw_probability(), so.additional_percents * 10 + so.PROBA_SUCCESS - 10)
		self.assertEqual(eo.get_raw_probability(), eo.additional_percents * 10 + eo.PROBA_SUCCESS - 10)


		dso2 = DataStealOrder(
			stealer_corporation=self.c2,
			player=self.p2,
			target_corporation=self.c,
			additional_percents=5,
		)
		dso2.clean()
		dso2.save()

		so2 = SabotageOrder(
			player=self.p2,
			target_corporation=self.c,
			additional_percents=5,
		)
		so2.clean()
		so2.save()

		eo2 = ExtractionOrder(
			player=self.p2,
			target_corporation=self.c,
			kidnapper_corporation=self.c2
		)
		eo2.clean()
		eo2.save()

		self.assertEqual(dso2.get_raw_probability(), dso2.additional_percents * 10 + dso2.PROBA_SUCCESS + 10)
		self.assertEqual(so2.get_raw_probability(), so2.additional_percents * 10 + so2.PROBA_SUCCESS + 10)
		self.assertEqual(eo2.get_raw_probability(), eo2.additional_percents * 10 + eo2.PROBA_SUCCESS + 10)

	def test_MDC_BANK_line_negative_effect(self):
		"""
		Test what happens when BANK party line is chosen to people who voted deregulation
		"""

		self.set_Turn_Line(MDCVoteOrder.BANK, MDCVoteOrder.BANK, MDCVoteOrder.DERE)

		self.g.resolve_current_turn()

		# Player 3 has voted Deregulation, so he shouldn't be able to speculate
		d = Derivative(name="first and last", game=self.g)
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
		Test what happens when the BANK party line is chosen
		"""

		self.set_Turn_Line(MDCVoteOrder.BANK, MDCVoteOrder.DERE, MDCVoteOrder.DERE)

		self.g.resolve_current_turn()

		# Player 1 has voted Garde Fous Bancaires, so he shouldn't be able to speculate
		d = Derivative(name="first and last", game=self.g)
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
