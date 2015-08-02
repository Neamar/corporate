from website.management.commands.stubgame import Command as StubGame
from engine_modules.vote.models import VoteOrder
from engine_modules.share.models import BuyShareOrder
from engine_modules.detroit_inc.models import DIncVoteOrder
from engine_modules.citizenship.models import CitizenshipOrder
# from engine_modules.corporation_run.models import SabotageOrder, DataStealOrder, ExtractionOrder
from django.db import transaction


class Command(StubGame):
	help = 'Create an advanced stub game for testing'

	def add_order(self, player, Order, **kwargs):
		o = Order(player=player, **kwargs)
		o.clean()
		o.save()

	@transaction.atomic
	def handle(self, *args, **options):
		super(Command, self).handle(*args, **options)

		self.g.disable_side_effects = True
		self.g.save()

		# Lets players do a lot of stuff
		self.g.player_set.all().update(money=10000)
		corporations = self.g.corporation_set.all()
		c1 = corporations[1]
		c1_market = c1.corporationmarket_set.first()
		c2 = corporations[2]
		c2_market = c2.corporationmarket_set.first()
		c3 = corporations[0]
		c3_market = c3.corporationmarket_set.first()

		# TURN 1
		# p1
		self.add_order(player=self.p1, Order=VoteOrder, corporation_market_up=c1_market, corporation_market_down=c2_market)
		self.add_order(player=self.p1, Order=BuyShareOrder, corporation=c1)
		self.add_order(player=self.p1, Order=DIncVoteOrder, coalition=DIncVoteOrder.CPUB)
		# self.add_order(player=self.p1, Order=SabotageOrder, target_corporation_market=c2_market)
		# p2
		self.add_order(player=self.p2, Order=VoteOrder, corporation_market_up=c2_market, corporation_market_down=c1_market)
		self.add_order(player=self.p2, Order=BuyShareOrder, corporation=c2)
		self.add_order(player=self.p2, Order=DIncVoteOrder, coalition=DIncVoteOrder.CPUB)
		# self.add_order(player=self.p2, Order=ExtractionOrder, target_corporation_market=c1_market, stealer_corporation=c2)

		# p3
		self.add_order(player=self.p3, Order=VoteOrder, corporation_market_up=c3_market, corporation_market_down=c2_market)
		self.add_order(player=self.p3, Order=BuyShareOrder, corporation=c3)
		self.add_order(player=self.p3, Order=DIncVoteOrder, coalition=DIncVoteOrder.CONS)
		# self.add_order(player=self.p3, Order=DataStealOrder, target_corporation_market=c1_market, stealer_corporation=c2)
		self.g.resolve_current_turn()
		self.stdout.write("Simulated turn #1")

		# TURN 2
		# p1
		self.add_order(player=self.p1, Order=VoteOrder, corporation_market_up=c1_market, corporation_market_down=c2_market)
		self.add_order(player=self.p1, Order=BuyShareOrder, corporation=c1)
		self.add_order(player=self.p1, Order=DIncVoteOrder, coalition=DIncVoteOrder.CPUB)
		self.add_order(player=self.p1, Order=CitizenshipOrder, corporation=c1)
		# self.add_order(player=self.p1, Order=SabotageOrder, target_corporation_market=c2_market)
		# p2
		self.add_order(player=self.p2, Order=VoteOrder, corporation_market_up=c2_market, corporation_market_down=c1_market)
		self.add_order(player=self.p2, Order=BuyShareOrder, corporation=c2)
		self.add_order(player=self.p2, Order=DIncVoteOrder, coalition=DIncVoteOrder.CONS)
		self.add_order(player=self.p2, Order=CitizenshipOrder, corporation=c2)
		# self.add_order(player=self.p2, Order=ExtractionOrder, target_corporation_market=c1_market, stealer_corporation=c2)

		# p3
		self.add_order(player=self.p3, Order=VoteOrder, corporation_market_up=c3_market, corporation_market_down=c2_market)
		self.add_order(player=self.p3, Order=BuyShareOrder, corporation=c3)
		self.add_order(player=self.p3, Order=DIncVoteOrder, coalition=DIncVoteOrder.CONS)
		self.add_order(player=self.p3, Order=CitizenshipOrder, corporation=c3)
		# self.add_order(player=self.p3, Order=DataStealOrder, target_corporation_market=c1_market, stealer_corporation=c2)
		self.g.resolve_current_turn()
		self.stdout.write("Simulated turn #2")

		self.g.disable_side_effects = False
		self.g.save()
