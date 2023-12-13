from day12_part1 import can_be_subgroup, pattern_groups_size


def test_groups_size():
    assert pattern_groups_size(list(".#.###.#####")) == [1, 3, 5]
    assert pattern_groups_size(list("#.###.#####")) == [1, 3, 5]
    assert pattern_groups_size(list("#.###.#####.")) == [1, 3, 5]
    assert pattern_groups_size(list("#.###.#####.?")) == [1, 3, 5]
    assert pattern_groups_size(list("#.?###.#####.?")) == [1]
    assert pattern_groups_size(list("#..#")) == [1, 1]


def test_can_be_supgroup():
    assert can_be_subgroup(group_size=[1, 2, 3], potential_supgroup=[1, 2, 3])
    assert can_be_subgroup(group_size=[1, 2, 3], potential_supgroup=[1, 2])
    assert not can_be_subgroup(group_size=[2, 2, 3], potential_supgroup=[1, 2])
