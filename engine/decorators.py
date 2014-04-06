def sender_instance_of(*args):
	"""
	Only call decorated function if sender is an instance of one of the specified class.
	"""
	Orders = args

	def d(func):
		def wrapper(*args, **kwargs):
			# Only validate for Offensive runs.
			for Order in Orders:
				if isinstance(kwargs['instance'], Order):
					func(*args, **kwargs)
					return
		return wrapper
	return d
