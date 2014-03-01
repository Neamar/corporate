import sys

from django.db import transaction
from django.test import TestCase

from engine.models import Game


class ModelTest(TestCase):
    """
    Inherit from test case, to retrieve all corporations
    """
    def setUp(self):
        self.g = Game()
        self.g.save()

    def test_corporations_first_effect(self):
        """
        Checking for all corporation first_effects
        """
        for corporation in self.g.corporation_set.all():
            sid = transaction.savepoint()
            try:
                corporation.on_first_effect()
            except:
                e = sys.exc_value
                message = "[%s.on_first_effect] %s" % (corporation.base_corporation_slug, str(e))
                raise e.__class__(message)
            transaction.savepoint_rollback(sid)

    def test_corporations_last_effect(self):
        """
        Checking for all corporation first_effects
        """
        for corporation in self.g.corporation_set.all():
            sid = transaction.savepoint()
            try:
                corporation.on_last_effect()
            except:
                e = sys.exc_value
                message = "[%s.on_last_effect] %s" % (corporation.base_corporation_slug, str(e))
                raise e.__class__(message)
            transaction.savepoint_rollback(sid)