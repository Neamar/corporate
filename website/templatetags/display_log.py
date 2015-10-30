from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag(name="display_log")
def display_log(log, display_context, delta_display=True, size="medium", color="white"):
	"""
	Handle whether the menu item should be the active one.
	Return "active" if that is the case, "" if not.
	The criterion here is whether the URL contains the keyword, not necessarily very robust.
	"""

	r = """<svg role="img" class="svg--%s svg--%s" title="%s"><use xlink:href="/static/img/sprite.svg#%s"></use></svg>""" % (size, color, escape(log.get_display(display_context)), log.event_type.lower())

	if delta_display:
		delta_type = ""
		if log.delta > 0:
			delta_type = "positive"
		else:
			delta_type = "negative"

		r += '<span class="%s">%s</span>' % (delta_type, log.delta)
	return r
