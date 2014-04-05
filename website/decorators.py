from django.shortcuts import render as django_render


def render(page):
	"""
	Render the page with returned dict.
	"""

	def decorator(func):
		def wrap(request, *a, **kw):
			response = func(request, *a, **kw)
			if isinstance(response, dict):
				return django_render(request, page, response)
			else:
				return response
		return wrap
	return decorator
