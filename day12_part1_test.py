from day12_part1 import (
    Record,
    arrangements_count,
    find_unknown_idx,
)


def test_arrangements_counts():
    line = "??? 1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts2():
    line = "#.# 1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts3():
    line = "#.? 1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts4():
    line = "?.# 1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts5():
    line = "?.? 1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts6():
    line = "#?? 1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts7():
    line = "#.#.### 1,1,3"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts8():
    line = ".??..??...?##. 1,1,3"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 4


def test_arrangements_counts9():
    line = "?#?#?#?#?#?#?#? 1,3,1,6"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts10():
    line = "????.#...#... 4,1,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts11():
    line = "????.######..#####. 1,6,5"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 4


def test_arrangements_counts12():
    line = "? 1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts13():
    line = "?? 1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 2


def test_arrangements_counts14():
    line = "??? 1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 3


# '#..' i '..#' ??


def test_arrangements_counts15():
    line = "?.? 1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 2


def test_arrangements_counts16():
    line = "??# 1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts17():
    line = "?.# 1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts18():
    line = "?###???????? 3,2,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 10


def test_arrangements_counts19():
    line = "?###??#????? 3,2,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 7


def test_arrangements_counts20():
    line = "?###??#??#?? 3,2,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 2


# ?###.##.???


def test_arrangements_counts21():
    line = "?##.??? 2,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 3


# ?##.#.? (2, 1)


def test_arrangements_counts22():
    # TODO: this should pass - make sure it does first
    line = "?##.#.? 2,1"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 1


def test_arrangements_counts23():
    # TODO: this should pass - make sure it does first
    line = ".??..??...?##..??..??...?##. 1,1,3,1,1,3"
    record = Record.from_line(line)
    line_count = arrangements_count(record.value, record.groups)
    assert line_count == 16


def test_find_unknown():
    # assert 0 == find_unknown_idx("?")
    assert 0 == find_unknown_idx("?#")
    assert 1 == find_unknown_idx("#?")
    assert 0 == find_unknown_idx("?##")
    assert 2 == find_unknown_idx("##?")
