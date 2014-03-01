from os import listdir

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from utils.read_markdown import read_markdown
from engine.models import Game


class BaseCorporation:
	"""
	Basic corporation definition, reused for each game
	Implemented as a separate non-model class to avoid cluttering the database
	"""

	BASE_CORPORATION_DIR = "%s/datas/corporations" % (settings.BASE_DIR)

	@classmethod
	def build_dict(cls):
		"""
		Build a dict holding all base corporations.
		This dict is static and will be available anytime.
		"""
		cls.base_corporations = {}
		for f in [f for f in listdir(cls.BASE_CORPORATION_DIR) if f.endswith('.md')]:
			bc = BaseCorporation(f[:-3])
			cls.base_corporations[bc.slug] = bc

	def __init__(self, slug):
		"""
		Create a base_corporation from a file
		"""
		path = "%s/%s.md" % (self.BASE_CORPORATION_DIR, slug)
		content, meta = read_markdown(path)
		self.meta = meta

		self.slug = slug
		self.name = meta['name'][0]
		self.description = mark_safe(content)

		self.datasteal = int(meta['datasteal'][0])
		self.sabotage = int(meta['sabotage'][0])
		self.extraction = int(meta['extraction'][0])
		self.detection = int(meta['detection'][0])

		code = "\n".join(meta['on_first'])
		self.on_first = self.compile_effect(code, "on_first")

		code = "\n".join(meta['on_last'])
		self.on_last = self.compile_effect(code, "on_last")

		try:
			self.initials_assets = int(meta['initials_assets'][0])
		except KeyError:
			self.initials_assets = 10

		try:
			self.derivative = meta['derivative'][0]
		except KeyError:
			# In the Model, the default value used to be 10
			self.derivative = 10

	def compile_effect(self, code, effect):
		"""
		Compile specified code. Effect is a string that will be used for stacktrace reports.
		"""
		return compile(code, "%s.%s()" % (self.name, effect), 'exec')

	@classmethod
	def retrieve_all(cls):
		return cls.base_corporations.values()

# Build the dict at startup once and for all
BaseCorporation.build_dict()


class Corporation(models.Model):
	"""
	A corporation being part of a game
	"""
	class Meta:
		unique_together = (('base_corporation_slug', 'game'), )

	base_corporation_slug = models.CharField(max_length=20)
	game = models.ForeignKey(Game)
	assets = models.SmallIntegerField()

	@cached_property
	def base_corporation(self):
		return BaseCorporation.base_corporations[self.base_corporation_slug]

	def on_first_effect(self, ladder):
		exec(self.base_corporation.on_first, {'game': self.game, 'corporations': self.game.corporation_set, 'ladder': ladder})

	def on_last_effect(self, ladder):
		exec(self.base_corporation.on_last, {'game': self.game, 'corporations': self.game.corporation_set, 'ladder': ladder})

	def update_assets(self, delta):
		"""
		Update assets values, and save the model
		"""
		self.assets += delta
		self.save()

	def __unicode__(self):
		return "%s (%s)" % (self.base_corporation.name, self.assets)
