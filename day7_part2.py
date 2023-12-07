# Day 7

import collections
from dataclasses import dataclass
import enum
import functools
import pathlib

# 252082465 is too high
# 251759939 is too high
# 251721105 is too high
# 250665248 is okay

_JOKER_SYMBOL = "J"

_LETTER_TO_VALUE = {
    _JOKER_SYMBOL: 0,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def is_joker(card: "Card") -> bool:
    return card.symbol == _JOKER_SYMBOL


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

    @functools.cached_property
    def value(self) -> int:
        if self.symbol.isdigit():
            return int(self.symbol)
        else:
            value = _LETTER_TO_VALUE.get(self.symbol)
            assert value is not None
            return value

    @staticmethod
    def from_symbol(s: str) -> "Card":
        return Card(symbol=s)

    def __hash__(self) -> int:
        return hash(self.symbol)

    def __lt__(self, other: "Card") -> bool:
        return self.value < other.value


@dataclass
class Hand:
    cards: tuple[Card, ...]
    bid: int

    def __hash__(self):
        return hash((self.cards, self.bid))

    @staticmethod
    def from_symbols(symbols: str, bid: int = 0) -> "Hand":
        assert len(symbols) == 5
        cards = tuple(Card.from_symbol(s) for s in symbols)
        return Hand(cards=cards, bid=bid)

    def _cards_for_hand_type(self) -> tuple[Card, ...]:
        card_for_jocker = self._most_common_card()
        if card_for_jocker is None:
            return self.cards

        return tuple((card_for_jocker if is_joker(c) else c) for c in self.cards)

    @functools.lru_cache
    def hand_type(self) -> HandType:
        cards_for_hand_type = self._cards_for_hand_type()

        distinct_cards = set(cards_for_hand_type)
        most_common_count = max(collections.Counter(cards_for_hand_type).values())

        # AAAAA
        if len(distinct_cards) == 1 and most_common_count == 5:
            return HandType.FIVE_OF_KIND
        # AAAAB
        elif len(distinct_cards) == 2 and most_common_count == 4:
            return HandType.FOUR_OF_KIND
        # AAABC
        elif len(distinct_cards) == 3 and most_common_count == 3:
            return HandType.THREE_OF_KIND
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

    def _most_common_card(self) -> Card | None:
        card_no_jocker = tuple(c for c in self.cards if not is_joker(c))
        if len(card_no_jocker) == 0:
            return None

        counter = collections.Counter(card_no_jocker)
        [(most_common_card, _)] = counter.most_common(1)

        assert not is_joker(most_common_card)

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
            if self_card == other_card:
                continue

            return self_card < other_card

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
