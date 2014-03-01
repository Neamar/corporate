from django.contrib import admin
from engine_modules.speculation.models import Derivative, CorporationSpeculationOrder, DerivativeSpeculationOrder

admin.site.register(Derivative)


class SpeculationOrderAdmin(admin.ModelAdmin):
	readonly_fields = ('on_win_ratio', 'on_loss_ratio')


admin.site.register(CorporationSpeculationOrder, SpeculationOrderAdmin)
admin.site.register(DerivativeSpeculationOrder, SpeculationOrderAdmin)
