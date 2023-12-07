from day7_part2 import Hand, HandType


def test_five_of_kind_with_jack():
    h1 = Hand.from_symbols("JJJ22")
    h2 = Hand.from_symbols("TTTKK")

    assert h1 > h2


def test_four_of_kind_with_jack():
    h1 = Hand.from_symbols("JJJ2A")
    h2 = Hand.from_symbols("TTTKK")

    assert h1 > h2


def test_three_of_kind_with_jack():
    h1 = Hand.from_symbols("JJ22A")
    h2 = Hand.from_symbols("TTJKK")

    assert h1 > h2


def test_two_fours_of_kind():
    h1 = Hand.from_symbols("33332")
    h2 = Hand.from_symbols("2AAAA")

    assert h1 > h2


def test_hand_type():
    assert Hand.from_symbols("QJJQ2").hand_type() == HandType.FOUR_OF_KIND
    assert Hand.from_symbols("32T3K").hand_type() == HandType.ONE_PAIR
    assert Hand.from_symbols("KK677").hand_type() == HandType.TWO_PAIR
    assert Hand.from_symbols("23432").hand_type() == HandType.TWO_PAIR
    assert Hand.from_symbols("T55J5").hand_type() == HandType.FOUR_OF_KIND
    assert Hand.from_symbols("KTJJT").hand_type() == HandType.FOUR_OF_KIND
    assert Hand.from_symbols("QQQJA").hand_type() == HandType.FOUR_OF_KIND


def test_hand_type_weaker():
    assert Hand.from_symbols("JKKK2") < Hand.from_symbols("QJJQ2")
    assert Hand.from_symbols("JJJJK") < Hand.from_symbols("JJKJJ")
