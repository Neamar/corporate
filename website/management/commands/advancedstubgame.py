from website.management.commands.stubgame import Command as StubGame
from engine_modules.vote.models import VoteOrder
from engine_modules.share.models import BuyShareOrder
from engine_modules.detroit_inc.models import DIncVoteOrder
from engine_modules.citizenship.models import CitizenshipOrder
# from engine_modules.corporation_run.models import SabotageOrder, DataStealOrder, ExtractionOrder


class Command(StubGame):
	help = 'Create an advanced stub game for testing'

	def handle(self, *args, **options):
		super(Command, self).handle(*args, **options)

		self.g.disable_side_effects = True
		self.g.save()

		corporations = self.g.corporation_set.all()
		c1 = corporations[1]
		c1_market = c1.corporationmarket_set.first()
		c2 = corporations[2]
		c2_market = c2.corporationmarket_set.first()
		c3 = corporations[0]
		c3_market = c3.corporationmarket_set.first()

		# TURN 1
		# p1
		VoteOrder.objects.create(player=self.p1, corporation_market_up=c1_market, corporation_market_down=c2_market)
		BuyShareOrder.objects.create(player=self.p1, corporation=c1)
		DIncVoteOrder.objects.create(player=self.p1, coalition=DIncVoteOrder.CPUB)
		CitizenshipOrder.objects.create(player=self.p1, corporation=c1)
		# SabotageOrder.objects.create(player=self.p1, target_corporation_market=c2_market)
		# p2
		VoteOrder.objects.create(player=self.p2, corporation_market_up=c2_market, corporation_market_down=c1_market)
		BuyShareOrder.objects.create(player=self.p2, corporation=c2)
		DIncVoteOrder.objects.create(player=self.p2, coalition=DIncVoteOrder.CPUB)
		CitizenshipOrder.objects.create(player=self.p1, corporation=c2)
		# ExtractionOrder.objects.create(player=self.p2, target_corporation_market=c1_market, stealer_corporation=c2)

		# p3
		VoteOrder.objects.create(player=self.p3, corporation_market_up=c3_market, corporation_market_down=c2_market)
		BuyShareOrder.objects.create(player=self.p3, corporation=c3)
		DIncVoteOrder.objects.create(player=self.p3, coalition=DIncVoteOrder.CONS)
		CitizenshipOrder.objects.create(player=self.p1, corporation=c3)
		# DataStealOrder.objects.create(player=self.p3, target_corporation_market=c1_market, stealer_corporation=c2)
		self.g.resolve_current_turn()

		self.g.disable_side_effects = False
		self.g.save()

		self.stdout.write("Simulated turn #1")
