"""Player game models."""
from multiset import Multiset

from resources import Resource
from game_models import GrowthCard, Nobleman, Hands


class Player(object):
    """Player model.

    resources: Multiset[Resource]
    cards: Multiset[GrowthCard]
    noblemen: Multiset[Nobleman]
    on_hands: Hands
    """

    def __init__(
            self,
            resources: Multiset[Resource],
            cards: Multiset[GrowthCard],
            noblemen: Multiset[Nobleman],
            on_hands: Hands,
    ):
        self.resources: Multiset[Resource] = resources
        self.cards: Multiset[GrowthCard] = cards
        self.noblemen: Multiset[Nobleman] = noblemen
        self.on_hands: Hands = on_hands

    @property
    def card_resources(self) -> Multiset[Resource]:
        return Multiset(map(lambda x: x.resource_type, self.cards))

    def validate_buy_card(self, card: GrowthCard) -> bool:
        new_price: Multiset[Resource] = card.price.difference(self.card_resources)
        return new_price.issubset(self.resources)

    def validate_gain_nobleman(self, nobleman: Nobleman) -> bool:
        return nobleman.price.issubset(self.card_resources)

    def buy_card(self, card: GrowthCard):
        if self.validate_buy_card(card):
            new_price: Multiset[Resource] = card.price.difference(self.card_resources)
            self.resources.difference_update(new_price)
            self.cards.add(card)
        else:
            raise ValueError('Not suffice resources.')

    def buy_card_from_hands(self, card: GrowthCard):
        if self.on_hands.validate_remove_card(card) and self.validate_buy_card(card):
            self.buy_card(card)
            self.on_hands.remove_card(card)
        else:
            raise ValueError('Not suffice resources or there are not on hands.')

    def gain_nobleman(self, nobleman: Nobleman):
        if self.validate_gain_nobleman(nobleman):
            self.noblemen.add(nobleman)
        else:
            raise ValueError('There are not the necessary cards.')
