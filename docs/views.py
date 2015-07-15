from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.utils.safestring import mark_safe

from utils.read_markdown import read_file_from_path, parse_markdown
from engine_modules.corporation.models import BaseCorporation


def index(request, page):
	if page == '':
		page = 'index'

	page = '%s/data/docs/%s.md' % (settings.BASE_DIR, page.replace('.', ''))

	raw = ""
	try:
		raw = read_file_from_path(page)
	except IOError:
		raise Http404("No documentation on this subject.")

	# Replace custom {{ corporations }} markup with a list of corporations:
	def list_corporation_as_markdown():
		strings = ["* [%s](corporations/%s.md)" % (c.name, c.slug) for c in BaseCorporation.retrieve_all()]
		return "\n".join(strings)
	raw = raw.replace('{{ corporations }}', list_corporation_as_markdown())
	content, metas = parse_markdown(raw)

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
