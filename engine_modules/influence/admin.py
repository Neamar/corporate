from django.contrib import admin

from engine_modules.influence.models import PlayerInfluence
from engine_modules.influence.orders import BuyInfluenceOrder

admin.site.register(PlayerInfluence)
admin.site.register(BuyInfluenceOrder)
