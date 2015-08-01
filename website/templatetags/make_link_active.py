from django import template

register = template.Library()


@register.simple_tag(takes_context=True, name="make_link_active")
def make_link_active(context, keyword):
	"""
	Handle whether the menu item should be the active one.
	Return "active" if that is the case, "" if not. 
	The criterion here is whether the URL contains the keyword, not necessarily very robust.
	"""

	request = context['request']

	if request.path.find(keyword) != -1:
		return "active"

	return '""'
