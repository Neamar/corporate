from django.shortcuts import render
from django.http import Http404
from django.conf import settings

def index(request, page):
	page = '%s/docs/markdown/%s.md' % (settings.BASE_DIR, page.replace('.', ''))

	try:
		with open(page, 'r') as content_file:
			content = content_file.read()
	except IOError:
		raise Http404("No documentation on this subject.")
	return render(request, 'docs/index.html', {"content": content})
