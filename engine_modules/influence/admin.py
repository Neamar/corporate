from django.contrib import admin

from engine_modules.influence.models import Influence
from engine_modules.influence.orders import BuyInfluenceOrder

admin.site.register(Influence)
admin.site.register(BuyInfluenceOrder)
