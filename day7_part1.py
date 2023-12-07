# Day 7

import collections
from dataclasses import dataclass
import pathlib

_LETTER_TO_VALUE = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

@dataclass
class Card:
    symbol: str
    value: int

    @staticmethod
    def from_symbol(s: str) -> 'Card':
        if s.isdigit():
            return Card(symbol=s, value=int(s))
        else:
            value = _LETTER_TO_VALUE.get(s)
            assert value is not None
            return Card(symbol=s, value=value)

    def __hash__(self) -> int:
        return hash(self.symbol)

@dataclass
class Hand:
    cards: tuple[Card, ...]
    bid: int

    def __repr__(self) -> str:
        cards_total = "".join(c.symbol for c in self.cards)
        bid = self.bid
        return f'Hand<{cards_total=}{bid=}>'

    def __lt__(self, other: 'Hand') -> bool:
        self_counts = sorted(collections.Counter(c.symbol for c in self.cards).values(), reverse=True)
        other_counts = sorted(collections.Counter(c.symbol for c in other.cards).values(), reverse=True)
        if self_counts == other_counts:
            for self_card, other_card in zip(self.cards, other.cards):
                if self_card.value == other_card.value:
                    continue

                return self_card.value < other_card.value

        return self_counts < other_counts


def main():
    data = pathlib.Path("day7_input.txt").read_text()
    items_raw = data.split('\n')

    hands: list[Hand] = []

    for item_raw in items_raw:
        cards_raw, bid_raw = item_raw.split(" ")
        cards = tuple(Card.from_symbol(c) for c in cards_raw)
        bid = int(bid_raw)

        hands.append(Hand(cards=cards, bid=bid))

    hands_sorted = sorted(hands)

    total_value = 0

    for idx, hand in enumerate(hands_sorted, 1):
        total_value += idx * hand.bid

    print(total_value)



if __name__ == "__main__":
    main()
