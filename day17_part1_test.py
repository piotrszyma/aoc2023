import textwrap

from day17_part1 import least_hit_loss_for_input


def test_case():
    data = "11\n11"""

    result = least_hit_loss_for_input(data)

    assert result == 2


def test_case_2():
    data = "119\n919\n911"""

    result = least_hit_loss_for_input(data)

    assert result == 4

def test_case_3():
    data = """
111111111
999999991
111111111
199999999
111111111
"""

    result = least_hit_loss_for_input(data)

    assert result == 4
