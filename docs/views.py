import markdown
import codecs

from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.utils.safestring import mark_safe

def index(request, page):
	if(page == ''):
		page = 'index'

	page = '%s/docs/markdown/%s.md' % (settings.BASE_DIR, page.replace('.', ''))

	raw = ''
	try:
		with codecs.open(page, encoding='utf-8') as content_file:
			for line in content_file:
				raw += line
	except IOError:
		raise Http404("No documentation on this subject.")

	md = markdown.Markdown(extensions=['nl2br', 'sane_lists', 'meta', 'table', 'footnotes'], safe_mode=True, enable_attributes=False)
	content = md.convert(raw)

	try:
		title = md.Meta['title'][0]
	except:
		title = "Corporate Game"

	content = mark_safe(content)

	return render(request, 'docs/index.html', {"content": content, "title": title})
