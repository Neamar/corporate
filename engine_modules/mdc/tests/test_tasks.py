from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.share.models import Share
from engine_modules.corporation.models import Corporation


class TaskTest(EngineTestCase):
    def setUp(self):
        
        super(TaskTest, self).setUp()

        self.p.money = 1000000
        self.p.save()

        self.p2 = Player(game=self.g, money=1000000)
        self.p2.save()

        self.g.corporation_set.all().delete()
        self.c = Corporation(base_corporation_slug='renraku', assets=20)
        self.g.corporation_set.add(self.c)
        self.c.share_set.all().delete()
        self.c2 = Corporation(base_corporation_slug='shiawase', assets=10)
        self.g.corporation_set.add(self.c2)
        self.c2.share_set.all().delete()

        self.s1 = Share(
            corporation=self.c,
            player=self.p,
            turn=self.g.current_turn
        )
        self.s1.save()

        self.s2 = Share(
            corporation=self.c,
            player=self.p,
            turn=self.g.current_turn
        )
        self.s2.save()

        self.v = MDCVoteOrder(
            player=self.p,
            party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[2][0]
        )
        self.v.save()

    def test_party_line_set(self):

        self.g.resolve_current_turn()
        line = (self.g.mdcvotesession_set.get(turn=self.g.current_turn)).current_party_line
        self.assertEqual(line, self.v.party_line)

    def test_equality_no_party_line(self):
    
        self.v2 = MDCVoteOrder(
            player=self.p,
            party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[3][0]
        )
        self.v2.save()
        self.g.resolve_current_turn()

        line = (self.g.mdcvotesession_set.get(turn=self.g.current_turn)).current_party_line
        self.assertEqual(line, MDCVoteOrder.MDC_PARTY_LINE_CHOICES[-1][0])
