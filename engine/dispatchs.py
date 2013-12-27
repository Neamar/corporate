import django.dispatch


"""
This signal gets sent when an order require validation (before save)
"""
validate_order = django.dispatch.Signal(providing_args=["instance"])


"""
This signal gets sent after a model is first saved in db
"""
post_create = django.dispatch.Signal(providing_args=["instance"])
