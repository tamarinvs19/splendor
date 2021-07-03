"""Base models of game objects."""
from __future__ import annotations

from multiset import Multiset

from resources import ResourceCollection, Resource


class HasPrestigePoint(object):
    """
    Interface for working with prestige point.

    prestige_point: int = 0
    """

    def __init__(self, prestige_point: int):
        self.prestige_point: int = prestige_point


class GrowthCard(HasPrestigePoint):
    """
    Growth game card.

    price: resources.ResourceCollection
    resource_type: resources.Resource
    prestige_point: int = 0
    """

    def __init__(self, price: ResourceCollection, resource_type: Resource, prestige_point: int = 0):
        super().__init__(prestige_point)
        self.price: ResourceCollection = price
        self.resource_type: Resource = resource_type


class Nobleman(HasPrestigePoint):
    """
    Nobleman game card.

    price: resources.ResourceCollection
    prestige_point: int = 3
    """

    def __init__(self, price: ResourceCollection):
        prestige_point: int = 3
        super().__init__(prestige_point)
        self.price: ResourceCollection = price

    def __eq__(self, other: Nobleman) -> bool:
        return self.price == other.price and self.prestige_point == other.prestige_point


class Hands(object):
    CARD_COUNTS: int = 3
    """
    Class <<Hands>> is equal a Multiset[GrowthCard] with size <= CARD_COUNTS.
    
    cards: Multiset[GrowthCard]
    """

    def __init__(self, cards: Multiset[GrowthCard]):
        self.cards: Multiset[GrowthCard]
        if len(self.cards) <= self.CARD_COUNTS:
            self.cards = cards
        else:
            raise ValueError('The number of the cards is very big. Maximum = {}'.format(self.CARD_COUNTS))

    def validate_add_card(self, _: GrowthCard) -> bool:
        return len(self.cards) < self.CARD_COUNTS

    def validate_remove_card(self, card: GrowthCard) -> bool:
        return card in self.cards

    def add_card(self, card: GrowthCard):
        if self.validate_add_card(card):
            self.cards.add(card)
        else:
            raise ValueError('The number of the cards is very big. Maximum = {}'.format(self.CARD_COUNTS))

    def remove_card(self, card: GrowthCard):
        if self.validate_remove_card(card):
            self.cards.remove(card)
        else:
            raise ValueError('This card does not exists in the hand.')