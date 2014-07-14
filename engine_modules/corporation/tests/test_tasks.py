from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation


class CrashRunTaskTest(EngineTestCase):
	def setUp(self):
		self.c = Corporation
