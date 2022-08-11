SUIT_IMPORTANCE = True

from django.conf import settings
from django.db import models
from django.db.models import expressions
from .cards import Deck

class CardField(models.CharField):
    def __init__(self, *args, suit_importance=None, **kwargs):
        kwargs['max_length'] = 30
        if suit_importance is None:
            if hasattr(settings, 'SUIT_IMPORTANCE'):
                self.suit_importance = settings.SUIT_IMPORTANCE
            else:
                self.suit_importance = SUIT_IMPORTANCE
        else:
            self.suit_importance = suit_importance
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ('suit_importance',)

    def from_db_value(self, value, expression, connection):
        if not isinstance(expression, expressions.Col):
            print('='*80)
            print(value, expression, connection)
        if value is None or value == "":
            return value
        return Deck(self.suit_importance).CARDS[value]

    def to_python(self, value):
        if isinstance(value, str):
            value = Deck(self.suit_importance).CARDS[value]
        return value

    def get_prep_value(self, value):
        return str(value)

    def get_lookup(self, lookup_name):
        found = super().get_lookup(lookup_name)
        print('-'*80)
        print(found)
        return found
