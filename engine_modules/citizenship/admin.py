from django.contrib import admin

from engine_modules.citizenship.models import CitizenShip
from engine_modules.citizenship.orders import CitizenShipOrder


admin.site.register(CitizenShip)
admin.site.register(CitizenShipOrder)