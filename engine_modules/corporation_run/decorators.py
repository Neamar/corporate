from engine_modules.corporation_run.models import ProtectionOrder


def override_max_protection(func):
	"""
	Ensure protection run always block
	"""
	def override_max_protection_wrapper(*args, **kwargs):
		# Needed to make the extraction fail unconditionally
		original_max_percents = ProtectionOrder.MAX_PERCENTS
		ProtectionOrder.MAX_PERCENTS = 0

		try:
			func(*args, **kwargs)
		finally:
			# Restore, whatever happens
			ProtectionOrder.MAX_PERCENTS = original_max_percents

	return override_max_protection_wrapper
