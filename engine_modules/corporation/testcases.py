from engine_modules.corporation.models import BaseCorporation
import copy


def override_base_corporations(func):
	"""
	Allow to override base corporation values for the length of a test.
	"""
	def base_corporation_wrapper(*args, **kwargs):
		original_base_corporations = copy.deepcopy(BaseCorporation.base_corporations)
		try:
			func(*args, **kwargs)
		finally:
			# Restore, whatever happens
			BaseCorporation.base_corporations = original_base_corporations

	return base_corporation_wrapper
