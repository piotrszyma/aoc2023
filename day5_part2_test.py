from day5_part2 import ItemMapping, difference, intersection


def test_no_overlap():
    assert difference(range(0, 10), range(10, 15)) == [range(0, 10)]


def test_left_overlap():
    #    -- r1 --
    #          - r2 -

    assert difference(range(0, 10), range(5, 15)) == [range(0, 5)]


def test_full_overlap():
    #         -- r1 --
    #          - r2 -
    assert difference(range(0, 10), range(1, 5)) == [range(0, 1), range(5, 10)]


def test_right_overlap():
    #           -- r1 --
    #          - r2 -

    assert difference(range(5, 10), range(0, 5)) == [range(5, 10)]

    #                   -- r1 --
    #          - r2 -


def test_regression():
    assert difference(range(100, 200), range(0, 5)) == [range(100, 200)]


def test_regression_2():
    assert difference(range(74, 88), range(77, 88)) == [range(74, 77)]


def test_regression_3():
    assert difference(range(57, 70), range(57, 61)) == [range(61, 70)]


def test_regression_4():
    assert difference(range(77, 88), range(77, 84)) == [range(84, 88)]

def test_old():
    # Tests.
    mapping1 = ItemMapping(dest_start=50, source_start=98, size=2)
    assert list(mapping1.range_) == [98, 99]

    mapping2 = ItemMapping(dest_start=52, source_start=50, size=48)
    assert mapping2.apply(79) == 81

    # right intersect
    assert intersection(range(0, 5), range(1, 6)) == range(1, 5)
    # all intersect
    assert intersection(range(0, 5), range(1, 4)) == range(1, 4)
    # left intersect
    assert intersection(range(-5, 6), range(0, 5)) == range(0, 5)
    # no intersect
    assert intersection(range(0, 5), range(6, 10)) == range(0, 0)

