import textwrap

from day17_part1 import least_hit_loss_for_input


def test_simple_case():
    data = "11\n11"""

    result = least_hit_loss_for_input(data)

    assert result == 2

