import django.dispatch

"""
This signal gets sent when an order require validation (before save)
"""
validate_order = django.dispatch.Signal(providing_args=["instance"])
