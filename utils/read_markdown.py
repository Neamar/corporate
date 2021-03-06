# -*- coding: utf-8 -*-
import re
import markdown
import codecs


def read_markdown(path):
	raw = read_file_from_path(path)

	return parse_markdown(raw)


def read_markdown_nullable(path):

	try:
		raw = read_file_from_path(path)
		html, _ = parse_markdown(raw)
	except IOError:
		html = ""
	
	return html


def parse_markdown(text):
	"""
	Convert markdown to html
	"""
	if text.strip() == '':
		return '', {}

	md = markdown.Markdown(extensions=['nl2br', 'sane_lists', 'meta', 'tables', 'toc'], safe_mode=False, enable_attributes=False)
	content = md.convert(text)

	content = re.sub(r'(\s|\()ny', u'\\1¥', content)
	return content, md.Meta


def read_file_from_path(path):
	raw = ''
	with codecs.open(path, encoding='utf-8') as content_file:
		for line in content_file:
			raw += line

		return raw
