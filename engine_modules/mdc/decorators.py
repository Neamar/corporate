def expect_coalition(coalition):
	"""
	Only call decorated function if coalition is the same as the order's game current_tyurn party line.
	To be used with valide_order
	"""
	def d(function):
		def wrapper(*args, **kwargs):
			instance = kwargs['instance']
			if instance.player.game.get_mdc_coalition() == coalition:
				function(*args, **kwargs)
		return wrapper
	return d
