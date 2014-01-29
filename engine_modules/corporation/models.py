import codecs
import markdown

from os import  listdir
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from engine.models import Game

BASE_CORPO_DIR = "%s/engine_modules/corporation/base_corporation" %(settings.BASE_DIR)

class BaseCorporation():
	"""
	Basic corporation definition, reused for each game
	Implemented as a separate non-model class to avoid cluttering the database
	"""

	def __init__(self, slug):

		path = "%s/%s.md" %(BASE_CORPO_DIR, slug)
		raw = ''
		
		with codecs.open(path, encoding='utf-8') as content_file:
			for line in content_file:
				raw += line

		md = markdown.Markdown(extensions=['nl2br', 'sane_lists', 'meta', 'tables', 'footnotes'], safe_mode=True, enable_attributes=False)
		content = md.convert(raw)

		self.name = md.Meta['name'][0]
		self.slug = md.Meta['slug'][0]
		try:
			self.initials_assets = int(md.Meta['initials_assets'][0], 10)
		except:
			# In the Model, the default value used to be 10
			self.initials_assets = 10

	@classmethod
	def retrieve_all(cls):
		return BASE_CORPORATIONS.values()
		
def build_corpo_dict():
	bc_dict = {}
	for f in listdir(BASE_CORPO_DIR):
		if f.endswith('.md'):
			bc = BaseCorporation(f.strip(".md"))
			bc_dict[bc.slug] = bc
	return bc_dict

BASE_CORPORATIONS = build_corpo_dict()

class Corporation(models.Model):
	"""
	A corporation being part of a game
	"""
	class Meta:
		unique_together = (('base_corporation_slug', 'game'), )

	base_corporation_slug = models.CharField(max_length=20)
	game = models.ForeignKey(Game)
	assets = models.PositiveSmallIntegerField()

	@cached_property
	def base_corporation(self):
		return BASE_CORPORATIONS[self.base_corporation_slug]

	def __unicode__(self):
		return "%s (%s)" % (self.base_corporation.name, self.game)

# TODO: move dat.
def get_ordered_corporations(self):
	return list(self.corporation_set.order_by('-assets'))
Game.get_ordered_corporations = get_ordered_corporations
