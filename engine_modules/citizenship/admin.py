from django.contrib import admin

from engine_modules.citizenship.models import Citizenship, CitizenshipOrder


admin.site.register(Citizenship)
admin.site.register(CitizenshipOrder)
