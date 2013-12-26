import django.dispatch

validate_order = django.dispatch.Signal(providing_args=["instance"])
