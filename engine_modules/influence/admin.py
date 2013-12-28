from django.contrib import admin

from engine_modules.influence.models import Influence, BuyInfluenceOrder


admin.site.register(Influence)
admin.site.register(BuyInfluenceOrder)
