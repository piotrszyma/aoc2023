from day12_part2 import Arrangement


def test_case1():
    assert Arrangement(
        items_to_process=["#", "?"],
        items_processed=[],
        current_item="#",
        groups_to_match=[1, 3, 6, 1],
        current_group_len=0,
    ).process() == [
        Arrangement(
            items_to_process=["?"],
            items_processed=["#"],
            current_item="#",
            groups_to_match=[1, 3, 6, 1],
            current_group_len=1,
        )
    ]


def test_case2():
    assert (
        Arrangement(
            items_to_process=["?"],
            items_processed=["#"],
            current_item="#",
            groups_to_match=[1, 3, 6, 1],
            current_group_len=1,
        ).process()
        == []
    )


# def test_case3():
#     a = Arrangement(
#         items_to_process=list("#?#?#?#?#?#?#?"),
#         items_processed=[],
#         current_item="?",
#         groups_to_match=[1, 3, 6, 1],
#         current_group_len=1,
#     )
#     assert Arrangement(
#         items_to_process=list("# ### ###### #"),
#         items_processed=[],
#         current_item="?",
#         groups_to_match=[1, 3, 6, 1],
#         current_group_len=1,
#     )
