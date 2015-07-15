from django import template

register = template.Library()


@register.simple_tag(takes_context=True, name="make_link_active")
def make_link_active(context, keyword):

	request = context['request']

	if request.path.find(keyword) != -1:
		return "active"

	return '""'
