from django.core.exceptions import ValidationError


class OrderNotAvailable(ValidationError):
	"""
	Exception thrown when an order is not available for use.
	"""
	pass
