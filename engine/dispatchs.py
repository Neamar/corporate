import django.dispatch


"""
This signal gets sent when an order require validation (before save)
"""
validate_order = django.dispatch.Signal(providing_args=["instance"])

"""
This signal gets sent after a model is first saved in db
"""
post_create = django.dispatch.Signal(providing_args=["instance"])

"""
This signal gets sent from the function create_game_event on Game.
"""
game_event = django.dispatch.Signal(providing_args=["game_event", "delta", "data", "corporation", "players", "corporation_market"])

"""
This signal gets sent from when the game starts
"""
start_event = django.dispatch.Signal(providing_args=["instance"])
