# -*- coding: utf-8 -*-
import re
import markdown
import codecs


def read_markdown(path):
	raw = ''
	with codecs.open(path, encoding='utf-8') as content_file:
		for line in content_file:
			raw += line

	md = markdown.Markdown(extensions=['nl2br', 'sane_lists', 'meta', 'tables', 'toc'], safe_mode=False, enable_attributes=False)
	content = md.convert(raw)

	content = re.sub(r'(\s|\()ny', u'\\1¥', content)

	return content, md.Meta