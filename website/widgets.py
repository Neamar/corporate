from django import forms


class PlainTextWidget(forms.TextInput):
	def render(self, name, value, attrs):
		return "%s" % value
		return super(PlainTextWidget, self).render(name, value, attrs)


class PlainTextField(forms.CharField):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('widget', PlainTextWidget)
		kwargs.setdefault('required', False)
		super(PlainTextField, self).__init__(*args, **kwargs)
