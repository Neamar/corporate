from django.contrib import admin
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder

admin.site.register(Derivative)
admin.site.register(CorporationSpeculationOrder)
