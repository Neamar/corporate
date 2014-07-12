# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.dispatchs import post_create

from engine.models import Game
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.market.models import CorporationMarket

@receiver(post_create, sender=Game)
def auto_create_corporation(sender, instance, **kwargs):
	"""
	Create influence model for new player
	Takes all the Base corporations and create corresponding Corporations
	"""
	instance.corporations = {}

	base_corporations = BaseCorporation.retrieve_all()
	for base_corporation in base_corporations:
		instance.corporations[base_corporation.slug] = Corporation(
			base_corporation_slug=base_corporation.slug,
			game=instance,
			assets=base_corporation.initials_assets
		)

		instance.corporations[base_corporation.slug].save()

		for market_name in base_corporation.market.keys():
			CorporationMarket(
				corporation = instance.corporations[base_corporation.slug],
				name=market_name, 
				value=base_corporation.market[market_name]
			).save()

