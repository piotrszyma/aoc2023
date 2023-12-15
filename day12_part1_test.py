from day12_part1 import Record, arrangements_count, find_unknown_idx


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

def test_find_unknown():
    # assert 0 == find_unknown_idx("?")
    assert 0 == find_unknown_idx("?#")
    assert 1 == find_unknown_idx("#?")
    assert 0 == find_unknown_idx("?##")
    assert 2 == find_unknown_idx("##?")
