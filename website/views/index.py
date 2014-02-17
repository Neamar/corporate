from __future__ import absolute_import
from django.shortcuts import render


def index(request):
	"""
	Welcome to the Corporate Game!
	"""
	return render(request, 'index.html', {})
