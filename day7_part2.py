# Day 7

import collections
from dataclasses import dataclass
import enum
import pathlib

# 252082465 is too high
# 251759939 is too high
# 251721105 is too high

_JACK_SYMBOL = "J"

_LETTER_TO_VALUE = {
    _JACK_SYMBOL: 0,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def is_jack(card: "Card") -> bool:
    return card.symbol == _JACK_SYMBOL


class HandType(enum.IntEnum):
    FIVE_OF_KIND = 6
    FOUR_OF_KIND = 5
    HOUSE = 4
    THREE_OF_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    ALL_DISTINCT = 0


@dataclass
class Card:
    symbol: str

    @property
    def value(self) -> int:
        if self.symbol.isdigit():
            return int(self.symbol)
        else:
            value = _LETTER_TO_VALUE.get(self.symbol)
            assert value is not None
            return value

    @staticmethod
    def from_symbol(s: str) -> "Card":
        if s.isdigit():
            return Card(symbol=s)
        else:
            value = _LETTER_TO_VALUE.get(s)
            assert value is not None
            return Card(symbol=s)

    def __hash__(self) -> int:
        return hash(self.symbol)

    def __lt__(self, other: "Card") -> bool:
        return self.value < other.value


@dataclass
class Hand:
    cards: tuple[Card, ...]
    bid: int

    def cards_for_hand_type(self) -> tuple[Card, ...]:
        card_for_jack = self.most_common_card()
        if card_for_jack is None:
            return self.cards

        return tuple((card_for_jack if is_jack(c) else c) for c in self.cards)

    def hand_type(self) -> HandType:
        distinct_cards = set(self.cards_for_hand_type())
        most_common_count = max(
            collections.Counter(self.cards_for_hand_type()).values()
        )

        # AAAAA
        if len(distinct_cards) == 1:
            return HandType.FIVE_OF_KIND
        # AAAAB
        elif len(distinct_cards) == 2 and most_common_count == 4:
            return HandType.FOUR_OF_KIND
        # AAABB
        elif len(distinct_cards) == 2 and most_common_count == 3:
            return HandType.HOUSE
        # AABBC
        elif len(distinct_cards) == 3:
            return HandType.TWO_PAIR
        # AABCD
        elif len(distinct_cards) == 4:
            return HandType.ONE_PAIR
        else:
            return HandType.ALL_DISTINCT

    @staticmethod
    def from_symbols(symbols: str, bid: int = 0) -> "Hand":
        assert len(symbols) == 5
        cards = tuple(Card.from_symbol(s) for s in symbols)
        return Hand(cards=cards, bid=bid)

    def most_common_card(self) -> Card | None:
        card_no_jack = tuple(c for c in self.cards if not is_jack(c))
        if len(card_no_jack) == 0:
            return None

        counter = collections.Counter(c for c in self.cards if not is_jack(c))
        [(most_common_card, _)] = counter.most_common(1)

        assert not is_jack(most_common_card)

        return most_common_card

    def __repr__(self) -> str:
        cards_total = "".join(c.symbol for c in self.cards)
        bid = self.bid
        return f"Hand<{cards_total=}{bid=}>"

    def __lt__(self, other: "Hand") -> bool:
        self_type = self.hand_type()
        other_type = other.hand_type()
        if self_type != other_type:
            return self_type < other_type

        # Same hand type.
        for self_card, other_card in zip(self.cards, other.cards):
            if self_card.value == other_card.value:
                continue

            return self_card.value < other_card.value

        raise ValueError(f"unexpected comparison {self=} {other=}")


def main():
    data = pathlib.Path("day7_input.txt").read_text()
    items_raw = data.split("\n")

    hands: list[Hand] = []

    for item_raw in items_raw:
        symbols, bid_raw = item_raw.split(" ")
        bid = int(bid_raw)
        hands.append(Hand.from_symbols(symbols, bid))

    hands_sorted = sorted(hands)

    total_value = 0

    for idx, hand in enumerate(hands_sorted, 1):
        total_value += idx * hand.bid

    print(total_value)


if __name__ == "__main__":
    main()
