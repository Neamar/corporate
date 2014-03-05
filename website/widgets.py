from django import forms
from django.utils.safestring import mark_safe


class PlainTextWidget(forms.TextInput):
	def render(self, name, value, attrs):
		return "%s" % value
		return super(PlainTextWidget, self).render(name, value, attrs)
