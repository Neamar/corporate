from __future__ import absolute_import
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.safestring import mark_safe
from django.db.models import Count
from engine_modules.citizenship.models import CitizenShip
from engine_modules.corporation.models import Corporation
from engine_modules.share.models import Share
from engine.models import Order, Player
from website.utils import get_player, get_orders_availability, get_order_by_name, get_shares_count
from utils.read_markdown import parse_markdown


def index(request):
	return render(request, 'index.html', {})
