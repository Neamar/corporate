from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.utils.safestring import mark_safe

from utils.read_markdown import read_markdown


def index(request, page):
	if(page == ''):
		page = 'index'

	page = '%s/docs/markdown/%s.md' % (settings.BASE_DIR, page.replace('.', ''))

	try:
		content, metas = read_markdown(page)
	except IOError:
		raise Http404("No documentation on this subject.")

	try:
		title = metas['title'][0]
	except:
		title = "Corporate Game"

	content = mark_safe(content)

	return render(request, 'docs/index.html', {"content": content, "title": title})
