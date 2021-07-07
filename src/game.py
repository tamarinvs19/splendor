"""Main game class"""
from multiset import Multiset

from src.game_field import ResourcesBank, NoblemenRow, GrowthCardsRow, GrowthCardsBank
from src.game_models import Nobleman, GrowthCard, Hands
from src.players import Player
from src.resources import ResourceCollection, Resource

InitPlayerType: (Multiset[Resource], Multiset[GrowthCard], Multiset[Nobleman], Multiset[GrowthCard])


class Splendor(object):
    def __init__(self,
                 init_resources: ResourceCollection,
                 init_noblemen: list[Nobleman],
                 init_growth_cards: list[list[GrowthCard]],
                 init_growth_banks: list[list[GrowthCard]],
                 init_players: list[InitPlayerType],
                 ):
        self.resources_bank: ResourcesBank = ResourcesBank(init_resources)
        self.noblemen: NoblemenRow = NoblemenRow(init_noblemen)
        self.growth_cards_banks: list[GrowthCardsBank] = [GrowthCardsBank(cards) for cards in init_growth_banks]

        self.growth_cards_rows: list[GrowthCardsRow] = []
        for bank, init_cards in zip(self.growth_cards_banks, init_growth_cards):
            self.growth_cards_rows.append(GrowthCardsRow(bank, init_cards))

        self.players: list[Player] = []
        for resources, growth_cards, noblemen, cards_on_hands in init_players:
            hands: Hands = Hands(cards_on_hands)
            self.players.append(Player(resources, growth_cards, noblemen, hands))
