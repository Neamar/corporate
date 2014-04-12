from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.utils.safestring import mark_safe

from utils.read_markdown import read_markdown
from engine_modules.corporation.models import BaseCorporation


def index(request, page):
	if page == '':
		page = 'index'

	page = '%s/datas/docs/%s.md' % (settings.BASE_DIR, page.replace('.', ''))

	try:
		content, metas = read_markdown(page)
	except IOError:
		raise Http404("No documentation on this subject.")

	try:
		title = metas['title'][0]
	except:
		title = "Corporate Game"

	title = mark_safe(title)
	content = mark_safe(content)

	return render(request, 'docs/index.html', {"content": content, "title": title})


def redirect_md(request, page):
	"""
	.md pages (for github compatibility)
	"""
	return redirect('docs.views.index', page=page)


def corporation(request, corporation_slug):
	"""
	Corporation pages
	"""

	try:
		base_corporation = BaseCorporation.base_corporations[corporation_slug]
	except KeyError:
		raise Http404("No matching corporation.")

	return render(request, 'docs/corporation.html', {"base_corporation": base_corporation})
