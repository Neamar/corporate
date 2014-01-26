import markdown
import codecs

from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.utils.safestring import mark_safe

def index(request, page):
	page = '%s/docs/markdown/%s.md' % (settings.BASE_DIR, page.replace('.', ''))

	raw = ''
	try:
		with codecs.open(page, encoding='utf-8') as content_file:
			for line in content_file:
				raw += line
	except IOError:
		raise Http404("No documentation on this subject.")

	content = markdown.markdown(raw, ['nl2br'], safe_mode=True, enable_attributes=False)
	content = mark_safe(content)

	return render(request, 'docs/index.html', {"content": content})
