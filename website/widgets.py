from django import forms


class PlainTextField(forms.CharField):
	def __init__(self, *args, **kwargs):
		# Closure for initial value (else displaying a bound form show None)
		class PlainTextWidget(forms.TextInput):
			def render(self, name, value, attrs):
				return kwargs['initial']
				return super(PlainTextWidget, self).render(name, value, attrs)

		kwargs.setdefault('widget', PlainTextWidget)
		kwargs.setdefault('required', False)
		super(PlainTextField, self).__init__(*args, **kwargs)
