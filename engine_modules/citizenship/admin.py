from django.contrib import admin

from engine_modules.citizenship.models import CitizenShip, CitizenShipOrder


admin.site.register(CitizenShip)
admin.site.register(CitizenShipOrder)
