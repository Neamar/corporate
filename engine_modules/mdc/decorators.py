def expect_party_line(party_line):
	"""
	Only call decorated function if party_line is the same as the order's game current_tyurn party line.
	To be used with valide_order
	"""
	def d(function):
		def wrapper(instance, *args, **kwargs):
			if instance.player.game.get_mdc_party_line() == party_line:
				function(instance, *args, **kwargs)
		return wrapper
	return d
