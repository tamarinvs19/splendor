"""Models for main game field"""
from src.resources import ResourceCollection, Resource, Gold
from src.game_models import GrowthCard, Nobleman


class ResourcesBank(object):
    MIN_FOR_DOUBLE: int = 4
    GOLD: Resource = Gold()

    def __init__(self, resources: ResourceCollection):
        self.resources: ResourceCollection = resources

    def validate_get_three(self, resource_types: set[Resource]) -> bool:
        return len(resource_types) == 3 and\
               all(resource_type in self.resources for resource_type in resource_types)

    def get_three(self, resource_types: set[Resource]) -> ResourceCollection:
        if self.validate_get_three(resource_types):
            self.resources.difference_update(resource_types)
            return ResourceCollection(resource_types)
        else:
            raise ValueError('Not enough resources.')

    def validate_get_two(self, resource_type: Resource) -> bool:
        return resource_type in self.resources and self.resources[resource_type] >= self.MIN_FOR_DOUBLE

    def get_two(self, resource_type: Resource) -> ResourceCollection:
        if self.validate_get_two(resource_type):
            double_set: ResourceCollection = ResourceCollection([resource_type] * 2)
            self.resources.difference_update(double_set)
            return double_set
        else:
            raise ValueError('Not enough resources.')

    def validate_get_gold(self) -> bool:
        return self.GOLD in self.resources

    def get_gold(self) -> ResourceCollection:
        if self.validate_get_gold():
            gold: ResourceCollection = ResourceCollection([Gold()])
            self.resources.difference_update(gold)
            return gold
        else:
            raise ValueError('Not enough gold.')


class GrowthCardsBank(object):
    def __init__(self, cards: list[GrowthCard]):
        self.cards: list[GrowthCard] = cards

    def validate_get_card(self) -> bool:
        return len(self.cards) > 0

    def get_card(self) -> GrowthCard:
        return self.get_cards(1)[0]

    def get_cards(self, number: int) -> list[GrowthCard]:
        if len(self.cards) >= number:
            return_cards: list[GrowthCard]
            self.cards, return_cards = self.cards[:number], self.cards[number:]
            return return_cards
        else:
            raise ValueError('Not enough cards.')


class GrowthCardsRow(object):
    def __init__(self, bank: GrowthCardsBank, init_cards: list[GrowthCard]):
        self.bank: GrowthCardsBank = bank
        self.cards: list[GrowthCard] = init_cards
        self.size: int = len(self.cards)

    def validate_remove_card(self, card: GrowthCard) -> bool:
        return card in self.cards

    def remove_card(self, card: GrowthCard) -> GrowthCard:
        if self.validate_remove_card(card):
            self.cards.remove(card)
            return card
        else:
            raise ValueError('There is not this card in this row.')

    def fill(self) -> None:
        card_number: int = self.size - len(self.cards)
        self.cards += self.bank.get_cards(card_number)


class NoblemenRow(object):
    def __init__(self, noblemen: list[Nobleman]):
        self.noblemen: list[Nobleman] = noblemen

    def validate_remove_nobleman(self, nobleman: Nobleman) -> bool:
        return nobleman in self.noblemen

    def remove_nobleman(self, nobleman: Nobleman) -> Nobleman:
        if self.validate_remove_nobleman(nobleman):
            self.noblemen.remove(nobleman)
            return nobleman
        else:
            raise ValueError('There is not this nobleman in this row.')

    def filter_by_resources(self, resources: ResourceCollection) -> list[Nobleman]:
        return list(filter(lambda nobleman: nobleman.price.issubset(resources), self.noblemen))
