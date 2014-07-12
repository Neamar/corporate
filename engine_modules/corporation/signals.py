# -*- coding: utf-8 -*-
from django.dispatch import receiver
from engine.dispatchs import post_create

from engine.models import Game
from engine_modules.corporation.models import BaseCorporation, Corporation
from engine_modules.market.models import Market, CorporationMarket


@receiver(post_create, sender=Game)
def auto_create_corporation(sender, instance, **kwargs):
	"""
	Create influence model for new player
	Takes all the Base corporations and create corresponding Corporations
	"""
	instance.corporations = {}
	markets = {}
	base_corporations = BaseCorporation.retrieve_all()

	# List distinct market types
	for base_corporation in base_corporations:
		for market_name in base_corporation.markets.keys():
			markets[market_name] = True

	# Save them on DB
	for market_name in markets.keys():
		markets[market_name] = Market(game=instance, name=market_name)
		markets[market_name].save()

	corporation_markets = []
	for base_corporation in base_corporations:
		instance.corporations[base_corporation.slug] = Corporation(
			base_corporation_slug=base_corporation.slug,
			game=instance,
			assets=base_corporation.initials_assets,
			historic_market=markets[base_corporation.historic_market]
		)

		instance.corporations[base_corporation.slug].save()

		for market_name in base_corporation.markets.keys():
			cm = CorporationMarket(
				corporation=instance.corporations[base_corporation.slug],
				market=markets[market_name],
				value=base_corporation.markets[market_name]
			)
			corporation_markets.append(cm)

	CorporationMarket.objects.bulk_create(corporation_markets)
