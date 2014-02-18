from django.contrib import admin
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder, DerivativeSpeculationOrder

admin.site.register(Derivative)
admin.site.register(CorporationSpeculationOrder)
admin.site.register(DerivativeSpeculationOrder)
