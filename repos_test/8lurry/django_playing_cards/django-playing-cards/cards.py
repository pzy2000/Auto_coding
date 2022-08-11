import random
system_random = random.SystemRandom()
from inspect import isclass

class Card(object):
    suit = None

    def __init__(self, suit=None):
        if suit is not None:
            self.suit = suit

    def __str__(self):
        name = self.__class__.__name__.lower()
        if self.suit is not None:
            name = name + 'Of' + self.suit.__class__.__name__
        return name

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        default = isinstance(other, self.__class__)
        if (not default or other.suit is None or self.suit is None
            or not self.suit.deck.SUIT_IS_IMPORTANT
            or not other.suit.deck.SUIT_IS_IMPORTANT
        ):
            return default
        return self.suit == other.suit

    def __lt__(self, other):
        return ORDER.find_index(self) < ORDER.find_index(other)

    def __le__(self, other):
        return ORDER.find_index(self) <= ORDER.find_index(other)

    def __gt__(self, other):
        return ORDER.find_index(self) > ORDER.find_index(other)

    def __ge__(self, other):
        return ORDER.find_index(self) >= ORDER.find_index(other)

class Ace(Card):
    pass

class King(Card):
    pass

class Queen(Card):
    pass

class Jack(Card):
    pass

class Ten(Card):
    pass

class Nine(Card):
    pass

class Eight(Card):
    pass

class Seven(Card):
    pass

class Six(Card):
    pass

class Five(Card):
    pass

class Four(Card):
    pass

class Three(Card):
    pass

class Two(Card):
    pass

BRIDGE = (
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Jack,
    Queen,
    King,
    Ace
)

class Order(object):
    suit = BRIDGE

    def find_index(self, card):
        for i, klass in enumerate(self.suit):
            if card == klass():
                return i

ORDER = Order()

class Suit(object):

    def __init__(self, deck):
        self.deck = deck
        self.order = Order()
        for card in self.order.suit:
            setattr(self, str(card()), card(self))

    def __eq__(self, other):
        return self.__class__ == other.__class__

class Spade(Suit):
    pass

class Club(Suit):
    pass

class Heart(Suit):
    pass

class Diamond(Suit):
    pass

class Deck(object):

    _deck = []
    _deck_dict = dict()
    SUIT_IS_IMPORTANT = True

    def __init__(self, suit_importance: bool = True):
        self._deck.clear()
        self.SUIT_IS_IMPORTANT = suit_importance
        self.spade = Spade(self)
        self.club = Club(self)
        self.heart = Heart(self)
        self.diamond = Diamond(self)
        for suit in [self.spade, self.club, self.heart, self.diamond]:
            for klass in ORDER.suit:
                item = getattr(suit, klass.__name__.lower())
                self._deck.append(item)
                self._deck_dict[str(item)] = item

    @property
    def CARDS(self):
        return self._deck_dict

    @property
    def full_deck(self):
        return self._deck

    def shuffle(self):
        system_random.shuffle(self._deck)
        return self.full_deck
